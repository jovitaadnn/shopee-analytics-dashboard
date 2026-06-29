from flask import Flask, render_template, request
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

df = pd.read_csv("dataset_stki.csv", sep=";")
df = df.fillna("")

df["content"] = (
    df["product_name"] + " " +
    df["category"] + " " +
    df["shop_name"] + " " +
    df["province"] + " " +
    df["city"] + " " +
    df["campaign_name"] + " " +
    df["campaign_type"] + " " +
    df["review_text"] + " " +
    df["delivery_status"]
)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["content"])

def search(query):
    # Ubah query menjadi vektor TF-IDF
    query_vector = vectorizer.transform([query])

    # Hitung cosine similarity
    similarity = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Tambahkan skor ke dataframe
    df_result = df.copy()
    df_result["score"] = similarity

    # Ambil hasil dengan skor > 0
    df_result = df_result[df_result["score"] > 0]

    # Urutkan dari yang paling relevan
    df_result = df_result.sort_values(by="score", ascending=False)

    # Ambil 10 hasil teratas
    return df_result.head(10)
    return result.head(10)

# ROUTES
# =======================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/business-intelligence")
def business():
    return render_template("business-intelligence.html")

@app.route("/customer-segmentation")
def segmentation():
    return render_template("customer-segmentation.html")

@app.route("/seller-performance")
def seller():
    return render_template("seller-performance.html")

@app.route("/sales-forecast")
def forecast():
    return render_template("sales-forecast.html")

@app.route("/information-retrieval", methods=["GET","POST"])
def retrieval():

    results = None

    if request.method == "POST":
        keyword = request.form["keyword"]
        results = search(keyword)

    return render_template(
        "information-retrieval.html",
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)