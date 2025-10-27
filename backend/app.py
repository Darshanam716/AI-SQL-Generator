from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from transformers import T5Tokenizer, T5ForConditionalGeneration
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Allow OAuth on localhost
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Load environment variables
load_dotenv()

# -------------------- Flask App Setup --------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

# -------------------- Google OAuth --------------------
google_bp = make_google_blueprint(
    client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
    client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_to="google_login"  # endpoint for redirect after login
)
app.register_blueprint(google_bp, url_prefix="/login")

# -------------------- Load AI SQL Model --------------------
# Use a pre-trained T5 SQL model from Hugging Face
model_path = "./model/t5_sql_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)


# -------------------- MongoDB Setup --------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["ai_sql_db"]
collection = db["queries"]
users_collection = db["users"]

# -------------------- Routes --------------------
@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/generate_sql", methods=["POST"])
def generate_sql():
    user_query = request.form.get("query", "").strip()
    if not user_query:
        return jsonify({"sql": "No query received."})

    # Add prefix for T5 SQL task
    input_text = "translate English to SQL: " + user_query
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate SQL
    output_ids = model.generate(
        input_ids,
        max_length=150,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2
    )
    sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Save query in MongoDB
    user_email = session.get("user", {}).get("email", "anonymous")
    collection.insert_one({
        "user_email": user_email,
        "user_query": user_query,
        "generated_sql": sql_query
    })

    return jsonify({"sql": sql_query})

# Google login
@app.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return f"Error fetching user info: {resp.text}"

    user_info = resp.json()
    # Store in session
    session["user"] = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        "picture": user_info.get("picture")
    }

    # Save user in MongoDB if not exists
    if not users_collection.find_one({"email": user_info.get("email")}):
        users_collection.insert_one({
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture")
        })

    return redirect(url_for("index"))

# Google OAuth authorized endpoint
@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return f"Error fetching Google profile info: {resp.text}"

    user_info = resp.json()
    session["user"] = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        "picture": user_info.get("picture")
    }

    # Save user in MongoDB
    if not users_collection.find_one({"email": user_info.get("email")}):
        users_collection.insert_one({
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture")
        })

    return redirect(url_for("index"))

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)







# from flask import Flask, render_template, request, jsonify
# from transformers import T5Tokenizer, T5ForConditionalGeneration
# import torch

# # Load your local model
# MODEL_PATH = "./model/t5_sql_model"
# tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
# model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate_sql', methods=['POST'])
# def generate_sql():
#     user_query = request.form.get('query', '').strip()
#     if not user_query:
#         return jsonify({"sql": "No query received."})

#     # Normalize operators in the prompt
#     normalized_query = user_query.lower()
#     if "more than" in normalized_query:
#         normalized_query = normalized_query.replace("more than", ">")
#     if "less than" in normalized_query:
#         normalized_query = normalized_query.replace("less than", "<")
#     if "equal to" in normalized_query:
#         normalized_query = normalized_query.replace("equal to", "=")

#     prompt = f"translate English to SQL: {normalized_query}"

#     # Tokenize and generate
#     inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
#     outputs = model.generate(
#         **inputs,
#         max_length=150,
#         num_beams=5,
#         early_stopping=True,
#         no_repeat_ngram_size=2
#     )
#     sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Replace generic 'table' with actual table name
#     sql_query = sql_query.replace("table", "employees")

#     return jsonify({"sql": sql_query})

# if __name__ == '__main__':
#     app.run(debug=True)


# from transformers import T5Tokenizer, T5ForConditionalGeneration
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# model_name = "mrm8488/t5-base-finetuned-wikiSQL"
# tokenizer = AutoTokenizer.from_pretrained("./model/t5_sql_model")
# model = AutoModelForSeq2SeqLM.from_pretrained("./model/t5_sql_model")


# print("Welcome to AI SQL Generator! Type 'exit' to quit.")

# while True:
#     query = input("\nEnter your question in English: ")
#     if query.lower() == "exit":
#         break

#     # Add a proper SQL prompt so the model knows what to generate
#     prompt = f"translate English to SQL: {query}"

#     inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

#     # Generate SQL
#     outputs = model.generate(
#         **inputs,
#         max_length=150,
#         num_beams=5,
#         early_stopping=True
#     )

#     # sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     # print("Generated SQL:", sql)
#     sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Basic post-processing to fix missing operators
#     if "WHERE" in sql and ">" not in sql and "<" not in sql:
#         if "more than" in query:
#             sql = sql.replace("Salary", "Salary >")
#         elif "less than" in query:
#             sql = sql.replace("Salary", "Salary <")

#     # Replace generic 'table' with actual table name
#     sql = sql.replace("table", "employees")

#     print("Generated SQL:", sql)
