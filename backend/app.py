from flask import Flask, request, jsonify
import allure
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Attach request details to Allure reports before each request
@app.before_request
def log_request_info():
    request_info = (
        f"Request URL: {request.url}\n"
        f"Request Method: {request.method}\n"
        f"Request Headers: {request.headers}\n"
        f"Request Body: {request.get_data(as_text=True)}"
    )
    allure.attach(request_info, name="Request Info", attachment_type=allure.attachment_type.TEXT)
    logger.info(f"Request Details: {request_info}")

# Home route
@app.route("/")
def home():
    message = "Welcome to the Travel Reservation System!"
    allure.attach(message, name="Homepage Message", attachment_type=allure.attachment_type.TEXT)
    logger.info("Accessed Home Page")
    return jsonify({"message": message})

# Booking route
@app.route("/book", methods=["POST"])
def book_destination():
    try:
        # Parse the request JSON
        data = request.json
        destination = data.get("destination", "Unknown")
        
        # Response structure
        response = {"status": "success", "destination": destination}
        
        # Attach response to Allure report
        allure.attach(str(response), name="Booking Response", attachment_type=allure.attachment_type.TEXT)
        
        # Log the booking action
        logger.info(f"User booked destination: {destination}")
        return jsonify(response)
    except Exception as e:
        # Handle errors and log them
        error_message = {"status": "error", "message": str(e)}
        allure.attach(str(error_message), name="Error Info", attachment_type=allure.attachment_type.TEXT)
        logger.error(f"Error occurred: {e}")
        return jsonify(error_message), 500

# Metrics route for Prometheus (optional)
@app.route("/metrics")
def metrics():
    try:
        # Example metric (bookings_total) for demonstration
        bookings_metric = "bookings_total{destination='Paris'} 10"
        allure.attach(bookings_metric, name="Metrics", attachment_type=allure.attachment_type.TEXT)
        logger.info("Accessed metrics endpoint")
        return bookings_metric, 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
        logger.error(f"Error fetching metrics: {e}")
        return jsonify(error_message), 500

# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
