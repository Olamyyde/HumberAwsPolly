from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form('text')
    polly_client = boto3.session().client('polly')
    response = polly_client.synthesize_speech(Text=text, VoiceId='Joanna', OutputFormat='mp3')
    audio = response['AudioStream'].read()
    with open('static/output.mp3', 'wb') as file:
        file.write(audio)
    return render_template

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
