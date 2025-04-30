from flask import Flask, render_template, request, redirect, url_for
import boto3
from datetime import datetime

app = Flask(__name__)

# Connect to DynamoDB in the correct region
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

# Define your tables
student_table = dynamodb.Table('student')
marks_table = dynamodb.Table('marks')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    regno = request.form['regno']
    name = request.form['name']
    standard = request.form['class']
    math = int(request.form['math'])
    english = int(request.form['english'])
    science = int(request.form['science'])
    computer = int(request.form['computer'])
    timestamp = datetime.now().isoformat()

    # Save student info
    student_table.put_item(
        Item={
            'id': regno,
            'name': name,
            'class': standard,
            'created_at': timestamp
        }
    )

    # Save marks
    marks_table.put_item(
        Item={
            'student_is': regno,
            'class': standard,
            'math': math,
            'english': english,
            'science': science,
            'computer': computer,
            'created_at': timestamp
        }
    )

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()