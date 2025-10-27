# 🤖 AI SQL Generator

AI SQL Generator is a smart web application that automatically converts **natural language queries (English)** into **SQL statements** using a fine-tuned **T5 Transformer model**.  
It includes **Google Login (OAuth 2.0)** for secure access and uses **MongoDB** to store user queries and generated SQL outputs.

---

## 🚀 Features

- 🧩 **AI-Powered SQL Generation:**  
  Converts plain English queries like *“Show employees whose salary is above 50000”* into valid SQL statements.

- 🔐 **Google OAuth Login:**  
  Users can log in securely using their Google account.

- 💾 **MongoDB Integration:**  
  Stores each user’s queries and generated SQL for later reference.

- 🧠 **Hugging Face T5 Model:**  
  Uses a Transformer-based model (`t5-small`) for English → SQL translation.

- 🌐 **Flask Backend:**  
  Built using Flask with REST APIs and template rendering.

---

## 🏗️ Project Structure

AI-SQL-Generator/
│
├── backend/
│ ├── app.py # Main Flask backend
│ ├── templates/
│ │ └── index.html # Frontend UI
│ ├── static/
│ │ └── style.css # Custom CSS
│ ├── model/
│ │ └── t5_sql_model/ # (optional) Fine-tuned local model
│ └── .env # Environment variables (client ID, secret key)
│
├── README.md
└── requirements.txt









---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Darshanam716/AI-SQL-Generator.git
cd AI-SQL-Generator/backend



2️⃣ Create Virtual Environment
python -m venv sqlenv
sqlenv\Scripts\activate   # On Windows
# or
source sqlenv/bin/activate  # On Mac/Linux


If you don’t have a requirements.txt, generate one:

pip freeze > requirements.txt

4️⃣ Setup .env File
#  setup sqlenv file with all required keys

Create a .env file inside backend/ folder:

SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://localhost:27017/
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

5️⃣ Configure Google OAuth 2.0

Go to Google Cloud Console
.

Create a new OAuth 2.0 Client ID (Web Application).

Add the following:

Authorized JavaScript origins:
http://127.0.0.1:5000

Authorized redirect URIs:

http://127.0.0.1:5000/login/google/authorized

http://localhost:5000/login/google/authorized

6️⃣ Run the Flask App
python app.py


Visit 👉 http://127.0.0.1:5000

🧪 Example Query

Input:

show all employees whose salary is more than 30000


Output:

SELECT * FROM employees WHERE salary > 30000;



🧰 Tech Stack
Component	Technology Used
Backend	Flask
Frontend	HTML, CSS, JS
Database	MongoDB
AI Model	T5 (Hugging Face Transformers)
Auth	Google OAuth 2.0
Language	Python 3.10+
🧑‍💻 Author

Darshan A M
📧 Email: amdarshan557@gmail.com

💼 GitHub: https://github.com/Darshanam716

⭐ Future Enhancements

Add support for multiple SQL dialects (MySQL, PostgreSQL, SQLite).

Provide table schema input for better query generation.

Build history dashboard with past generated queries.


🎉 Enjoy your AI-powered SQL generator! If you encounter any issues or have suggestions, feel free to open an issue on this repository.
