from flask import Flask, render_template, request, jsonify
import allure
import logging

app = Flask(__name__)

# Configure logging for Allure
logging.basicConfig(level=logging.INFO)

# Attach request details before each request
@app.before_request
def log_request_info():
    allure.attach(
        f"Request URL: {request.url}\n"
        f"Request Method: {request.method}\n"
        f"Request Headers: {request.headers}\n"
        f"Request Body: {request.get_data(as_text=True)}",
        name="Request Info",
        attachment_type=allure.attachment_type.TEXT
    )

# Home route
@app.route('/')
def home():
    message = "Welcome to the Travel Reservation System!"
    allure.attach(message, name="Homepage Message", attachment_type=allure.attachment_type.TEXT)
    return render_template('index.html', message=message)

# Destinations route
@app.route('/destinations')
def destinations():
    allure.attach("Navigated to destinations page", name="Destinations Info", attachment_type=allure.attachment_type.TEXT)
    return render_template('destinations.html')

# Book route
@app.route('/book', methods=["POST"])
def book_destination():
    data = request.json
    destination = data.get("destination", "Unknown")
    response = {"status": "success", "destination": destination}
    allure.attach(str(response), name="Booking Response", attachment_type=allure.attachment_type.TEXT)
    return jsonify(response)

# About route
@app.route('/about')
def about():
    allure.attach("Navigated to about page", name="About Info", attachment_type=allure.attachment_type.TEXT)
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
