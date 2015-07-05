from flask import Flask

# Create application object
app = Flask(__name__)

# Using decorators, link the application to a url
@app.route("/")
@app.route("/main")

# Define the view using a function, which returns a string
def view_week():
    return "The week's WOD go here."

# Start the development server using the run() method:
if __name__ == "__main__":
    app.run()
