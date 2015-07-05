from flask import Flask
from pytumblr import TumblrRestClient

# Create application object
app = Flask(__name__)

# Error Handling
app.config["DEBUG"] = True

# Using decorators, link the application to a url
@app.route("/")
@app.route("/main")

# Define the view using a function, which returns a string
def view_week():

    client = TumblrRestClient(
        'q3K5ba44O1DLAv39TDsp4fEMNY1pGAdXsiciIQQqZdAsXF54Zt',
        'UnkAeG6I7PRHidVqikB3zcrL6DI94q0woJv5sIeUCj3B7ndCdJ',
        'KT75Gar86W3elQAuU7VyiT9UUstfX6JAFGTvG01pJYKStqlAXN',
        'ZggEOt83VSC2lzvN01SWmFJy98r13oeuWyciXxfxVqOwAvo81n'
    )

    print client.info()

    last_seven_posts_json = client.posts('cfsacompetition.tumblr.com', type='text', limit=7)

    return str(last_seven_posts_json)

@app.route("/name/<name>")
def index(name):
    if name.lower() == "mehdi":
        return "Hello, {}".format(name), 200
    else:
        return "Not Found", 404

# Start the development server using the run() method:
if __name__ == "__main__":
    app.run()
