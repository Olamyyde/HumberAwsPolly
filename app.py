from flask import Flask, request, render_template, send_from_directory, redirec>
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys

app = Flask(__name__)


polly = boto3.client("polly", region_name='ca-central-1')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        return "Error: Could not synthesize speech."

    # Access the audio stream from the response
    if "AudioStream" in response:
        output = os.path.join('static', 'speech.mp3')
        try:
            # Open a file for writing the output as a binary stream
            with closing(response["AudioStream"]) as stream:
                with open(output, "wb") as file:
                    file.write(stream.read())
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            return "Error: Could not write to file."
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        return "Error: Could not stream audio."

    return redirect(url_for('result'))

@app.route('/result')
def result():
    audio_file = url_for('static', filename='speech.mp3')
    return render_template('result.html', audio_file=audio_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    print("Commit message: Added speech synthesis feature using AWS Polly and error handling.")
    print("Commit message: Implemented speech synthesis using AWS Polly and added error handling for file and stream operations.")
