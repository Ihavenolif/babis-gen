import openai
import os
import random
from flask import Flask, render_template, request

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if(request.method == "GET"):
        return render_template("index.html", number=random.randint(1,5))
    
    query = request.json["query"]

    if not query.endswith("?"):
        query = query + "?"

    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = "Respond to this question like Andrej Babiš in the latest presidential debate. Include recent news about presidential elections in the Czech republic. Respond in Czech. Make a lot of excuses. Be very mean and rude. Sound angry and annoyed. Don't talk directly about the topic.\n\n" + query,
        temperature=0.9,
        max_tokens=500
    )
    response_text = response.get("choices")[0].get("text")

    final_text = ""

    response_split = response_text.split(" ")

    for x in response_split:
        if ("te" in x or "de" in x or "ne" in x) and random.random() < 0.2:
            final_text += x.replace("te", "tě").replace("de", "dě").replace("ne", "ně") + " "
        else:
            final_text += x + " "

    return final_text

@app.route("/faq")
def faq():
    return render_template("faq.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)