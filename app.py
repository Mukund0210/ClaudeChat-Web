from flask import Flask, render_template, request
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

model = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        response = get_anthropic_response(user_input)
    return render_template("index.html", response=response)
    
def get_anthropic_response(prompt):
    response = model.messages.create(
        model = "claude-3-7-sonnet-20250219",
        max_tokens= 1024,
        temperature= 0.7,
        messages=[
            {"role": "user", "content" : prompt}
        ]
    )
    
    return response.content[0].text

if __name__ == "__main__":
    app.run(debug=True)