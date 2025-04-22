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
        body { 
            font-family: 'Comic Sans MS', cursive; 
            background: url("https://i.pinimg.com/originals/c3/0c/e8/c30ce876948646203d29f46dffd040d8.jpg") no-repeat center fixed; 
            background-size: cover; 
            margin: 0; 
            padding: 0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.2); /* Lighter overlay for better visibility */
            z-index: -1;
        }
        .chat-box { 
            max-width: 600px; 
            width: 90%; 
            background: rgba(255, 255, 255, 0.75); /* Slightly more transparent white background */
            padding: 1.5rem; 
            border-radius: 1rem; 
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2); 
        }
        .messages { 
            height: 300px; 
            overflow-y: auto; 
            border: 1px solid #ccc; 
            padding: 1rem; 
            border-radius: 0.5rem; 
            background: rgba(240, 248, 255, 0.8); /* Light blue background for messages */
        }
        .msg { 
            margin: 0.5rem 0; 
        }
        .msg.user { 
            text-align: right; 
            color: #333; 
        }
        .msg.doraemon { 
            color: #007BFF; 
        }
        input[type="text"] { 
            width: calc(100% - 100px); 
            padding: 0.5rem; 
            border: 1px solid #ccc; 
            border-radius: 0.3rem; 
            margin-right: 0.5rem; 
        }
        button { 
            padding: 0.5rem 1rem; 
            background: #007BFF; 
            color: white; 
            border: none; 
            border-radius: 0.3rem; 
            cursor: pointer; 
            transition: background 0.3s ease; 
        }
        button:hover { 
            background: #0056b3; 
        }
        h1 { 
            color: white; 
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); 
            margin-bottom: 1rem; 
        }
    </style>
</head>
<body>
    <div class="overlay"></div>
    <div class="chat-box">
        <h1>🤖 Doraemon Chatbot</h1>
        <div class="messages" id="messages"></div>
        <div style="margin-top: 1rem;">
            <input type="text" id="userInput" placeholder="Ask Doraemon something..." />
            <button onclick="sendMessage()">Send</button>
        </div>
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
        // Add event listener for the Enter key
        userInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
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