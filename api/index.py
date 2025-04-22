from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# Define the prompt template
prompt = PromptTemplate.from_template(
    "You are Doraemon, the robotic cat from the future. Answer this question like Doraemon: {question}"
)

# Create the chain
chain = prompt | llm | StrOutputParser()

# HTML template (Doraemon style)
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doraemon Chatbot</title>
    <style>
        body { font-family: 'Comic Sans MS', cursive; background: #D0E7FF; text-align: center; padding: 2rem; }
        .chat-box { max-width: 800px; margin: 0 auto; background: white; padding: 1rem; border-radius: 1rem; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .messages { height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 1rem; border-radius: 0.5rem; text-align: left; background: #F0F8FF; }
        .msg { margin: 0.5rem 0; }
        .msg.user { text-align: right; }
        .msg.doraemon { color: blue; }
        input[type="text"] { width: 80%; padding: 0.5rem; }
        button { padding: 0.5rem 1rem; background: #3399FF; color: white; border: none; border-radius: 0.3rem; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🤖 Doraemon Chatbot</h1>
    <div class="chat-box">
        <div class="messages" id="messages"></div>
        <input type="text" id="userInput" placeholder="Ask Doraemon something..." />
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const messagesDiv = document.getElementById("messages");

        function sendMessage() {
            const input = document.getElementById("userInput");
            const text = input.value;
            if (!text.trim()) return;

            const userMsg = `<div class='msg user'><strong>You:</strong> ${text}</div>`;
            messagesDiv.innerHTML += userMsg;
            input.value = "";

            fetch("/api/doraemon", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: text })
            })
            .then(res => res.json())
            .then(data => {
                const doraemonMsg = `<div class='msg doraemon'><strong>Doraemon:</strong> ${data.answer}</div>`;
                messagesDiv.innerHTML += doraemonMsg;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(template)

@app.route("/api/doraemon", methods=["POST"])
def doraemon_api():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."}), 400

    try:
        response = chain.invoke({"question": question})
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/about')
def about():
    return 'about page'