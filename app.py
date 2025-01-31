from flask import Flask, request, jsonify
import base64
import filetype

app = Flask(__name__)

# Helper function to validate and process file from base64
def process_file(file_b64):
    try:
        # Decode the base64 file string
        file_data = base64.b64decode(file_b64)
        # Use filetype to guess the MIME type
        kind = filetype.guess(file_data)
        mime_type = kind.mime if kind else 'unknown'
        # Calculate file size in KB
        file_size_kb = len(file_data) / 1024
        return True, mime_type, round(file_size_kb, 2)
    except Exception as e:
        return False, None, 0

@app.route('/bfhl', methods=['POST', 'GET'])
def process_data():
    if request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

    if request.method == 'POST':
        try:
            data = request.json.get("data", [])
            file_b64 = request.json.get("file_b64", None)

            # Hardcoded user details
            user_id = "john_doe_17091999"
            email = "john@xyz.com"
            roll_number = "ABCD123"

            # Split data into numbers and alphabets
            numbers = [item for item in data if item.isdigit()]
            alphabets = [item for item in data if item.isalpha()]
            lowercase_alphabets = [char for char in alphabets if char.islower()]
            highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else None

            # Process the file if file_b64 is provided
            if file_b64:
                file_valid, file_mime_type, file_size_kb = process_file(file_b64)
            else:
                file_valid = False
                file_mime_type = None
                file_size_kb = None

            response = {
                "is_success": True,
                "user_id": user_id,
                "email": email,
                "roll_number": roll_number,
                "numbers": numbers,
                "alphabets": alphabets,
                "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else [],
                "file_valid": file_valid,
                "file_mime_type": file_mime_type,
                "file_size_kb": file_size_kb
            }

            return jsonify(response), 200

        except Exception as e:
            return jsonify({"is_success": False, "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
