from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL configuration using environment variables
db_config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}

@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    text = data.get("text")
    reason = data.get("reason")
    image = data.get("image")
    server_source = data.get("server_source")
    model = data.get("model")

    # Insert data into MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO reports (text, reason, image, server_source, model)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (text, reason, image, server_source, model))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Report submitted successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    