from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

app = Flask(__name__)

# Initialize Claude with correct model name
llm = ChatAnthropic(
    anthropic_api_key=api_key,
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    temperature=0.7
)

memory = ConversationBufferMemory()

# Initialize conversation chain
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        response = conversation.invoke({"input": user_input})["response"]
        
    return render_template("index.html", response=response)
    
if __name__ == "__main__":
    app.run(debug=True)