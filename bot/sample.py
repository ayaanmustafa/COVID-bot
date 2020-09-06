from flask import Flask,render_template,request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__) 

bot = ChatBot("Chatterbot",storage_adapter="chatterbot.storage.SQLStorageAdapter",
	              read_only=True,
              filters = ["chatterbot.filters.RepetitiveResponseFilter"],
              preprocessors=['chatterbot.preprocessors.clean_whitespace'],
              logic_adapter=[
              {
                  'import_path':"chatterbot.logic.BestMatch",
                  'statement_comparison_function':"chatterbot.comparison.levenshtein_distance",
                  'response_selection_method':"chatterbot.response_selection.get_first_response"
              },
              {
                  'import_path':"chatterbot.logic.LowConfidenceAdapter",
                  'threshold':0.65,
                  'default_response':'Sorry I do not know that'
              }])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("data/data.yml")


@app.route("/")
def index():
     return render_template("index.html")#send context to html

@app.route("/get")
def get_bot_response():
     userText = request.args.get("msg") #get data from input,we write js  to index.html
     return str(bot.get_response(userText))


if __name__ == "__main__":
     app.run(debug = True)


