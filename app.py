import pandas as pd
import re 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

data = pd.read_csv("spam.csv", encoding="latin-1")
data = data[["v1", "v2"]].dropna()
data.columns = ["label", "message"]
data["message"] =  data["message"].astype(str)

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]","",text)
    text = re.sub(r"\s+"," ",text).strip()
    return text

data["message"]=data["message"].apply(preprocess)
data = data[data["message"]!=""]

X = data["message"]
y = data["label"].str.lower().map({"ham":"Not Spam","spam":"Spam"})

valid = y.notna()

X,y = X[valid], y[valid]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2, random_state = 42, stratify = y)

model = Pipeline([
    ("Vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB())
])

model.fit(X_train, y_train)
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Test accuracy:{accuracy:.2%}")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():
    data = request.get_json()
    message = data.get("message","")
    if not message.strip():
        return jsonify({"error":"Please enter a message"}), 400

    cleaned = preprocess(message)
    prediction = model.predict([cleaned])[0]

    return jsonify({"prediction":prediction})

if __name__ == "__main__":
    app.run(debug =True)