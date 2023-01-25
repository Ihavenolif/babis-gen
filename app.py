import openai
import os
from flask import Flask, render_template, request

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if(request.method == "GET"):
        return render_template("index.html")
    
    query = request.json["query"]

    if not query.endswith("?"):
        query = query + "?"

    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = "Respond to this question like Andrej Babiš. Respond in Czech. Make a lot of excuses.\n\n" + query,
        temperature=0.75,
        max_tokens=500
    )
    response_text = response.get("choices")[0].get("text")

    return response_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)