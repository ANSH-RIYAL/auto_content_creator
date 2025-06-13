from flask import Flask, render_template, request, send_file, jsonify
import os
from main import make_video, list_background_videos, list_background_music

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of available background videos
    videos = list_background_videos()
    # Get list of available background music
    music_files = list_background_music()
    return render_template('index.html', videos=videos, music_files=music_files)

@app.route('/create_video', methods=['POST'])
def create_video():
    try:
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        background_video = request.form.get('background_video')
        background_music = request.form.get('background_music')
        font_size = int(request.form.get('font_size', 96))  # Default to 96 if not provided
        
        if not all([title, content, background_video]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate font size
        if not (48 <= font_size <= 144):
            return jsonify({'error': 'Font size must be between 48 and 144'}), 400
        
        # Create video
        output_path = make_video(
            title=title,
            content=content,
            background_video=background_video,
            font_size=font_size,
            background_music=background_music if background_music != 'none' else None
        )
        
        # Return success response with the video path
        return jsonify({
            'success': True,
            'message': 'Video created successfully',
            'video_path': output_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 