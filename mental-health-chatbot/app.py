from flask import Flask, request, jsonify
import pandas as pd
import json
from flask_cors import CORS  # To allow cross-origin requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Only allow requests from the frontend

# Load the first CSV dataset (for chatbot responses)
csv_data_1 = pd.read_csv('Mental_Health_FAQ.csv')

# Load the second CSV dataset (for chatbot statements)
csv_data_2 = pd.read_csv('Combined_Data.csv')

# Clean both CSV datasets
csv_data_1['Questions'] = csv_data_1['Questions'].str.strip().str.lower()
csv_data_1['Answers'] = csv_data_1['Answers'].str.strip()
csv_data_2['statement'] = csv_data_2['statement'].str.strip().str.lower()
csv_data_2['status'] = csv_data_2['status'].str.strip()

# Load the JSON dataset (for chatbot intents)
with open('KB.json', 'r') as file:
    json_data = json.load(file)

# Access the 'intents' key (contains chatbot data)
intents = json_data['intents']

# Function to get a response based on user input (from JSON data)
def get_response_from_json(user_input):
    for intent in intents:
        for pattern in intent['patterns']:
            if user_input.lower() in pattern.lower():  # Match the pattern (case-insensitive)
                return intent['responses'][0]  # Return the first response for the matched pattern
    return None

# Function to get answer from CSV dataset
def get_answer_from_csv(user_input):
    for index, row in csv_data_1.iterrows():
        if user_input.lower() in row['Questions'].lower():  # Match the question (case-insensitive)
            return row['Answers']  # Return the answer from the CSV dataset
    return None

# Main function to get a response from either JSON or CSV
def get_response(user_input):
    response = get_response_from_json(user_input)
    if response:
        return response

    response = get_answer_from_csv(user_input)
    if response:
        return response

    if "recommend a doctor" in user_input.lower():
        doctor_id = 1  # Example doctor ID
        return f"I recommend Dr. Kavita Mehra. You can view her profile [here](http://localhost:3000/doctors/{doctor_id})."
    
    return "Sorry, I didn't understand that."

# Route for the chatbot
@app.route('/get-response', methods=['POST'])
def get_bot_response():
    user_input = request.json['input']
    print(f"Received input: {user_input}")  # Debugging statement
    response = get_response(user_input)
    return jsonify({'response': response})

# Route for getting a doctor's profile
@app.route('/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_profile(doctor_id):
    doctors = [
        {
            "id": 1,
            "name": "Dr. Kavita Mehra",
            "specialty": "General Mental Health",
            "experience": "10 years",
            "contact": "+91-9876543210",
            "address": "123 Wellness Road, New Delhi",
            "image_url": "https://example.com/dr-mehra.jpg"
        },
        {
            "id": 2,
            "name": "Dr. Rahul Sharma",
            "specialty": "Psychiatrist",
            "experience": "15 years",
            "contact": "+91-9876543211",
            "address": "456 Health Avenue, Mumbai",
            "image_url": "https://example.com/dr-sharma.jpg"
        }
    ]
    
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({"error": "Doctor not found"}), 404

# New Route for booking an appointment
@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    # Extract appointment details from the request
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    reason = data.get('reason')
    doctor_id = data.get('doctor_id')

    # Here, you could add code to save the appointment to a database.
    # For now, we'll just print it out to simulate saving.
    print(f"New appointment: {name}, {email}, {date}, {reason}, doctor_id: {doctor_id}")

    # Respond with a success message
    return jsonify({"message": "Appointment booked successfully"}), 200

# Home route (optional, can serve a landing page for your API)
@app.route('/')
def home():
    return '''<h1>Welcome to the Inner Voice API</h1>
              <p>Use /get-response for chatbot and /doctor/<id> for doctor profiles.</p>'''

if __name__ == '__main__':
    app.run(debug=True)
