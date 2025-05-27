from flask import Flask, render_template, request, send_file
import os
from main import make_video

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_ready = False
    video_path = None
    if request.method == 'POST':
        passage = request.form['passage']
        font_size = int(request.form.get('font_size', 48))
        output_path = 'final_video.mp4'
        make_video(passage, output_path=output_path, font_size=font_size)
        video_ready = True
        video_path = output_path
    return render_template('index.html', video_ready=video_ready, video_path=video_path)

@app.route('/download')
def download():
    return send_file('final_video.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 