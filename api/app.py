# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request, Response, send_file
from flask_cors import CORS
import yt_dlp
import tempfile

app = Flask(__name__)
CORS(app)

api_key = os.getenv("YOUTUBE_API_KEY")


def download_youtube_video(url):
    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, 'downloaded_video.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Find the downloaded file
        for file in os.listdir(temp_dir):
            if file.startswith('downloaded_video'):
                return os.path.join(temp_dir, file)
        return None
    except Exception as e:
        return str(e)


@app.route('/searchvideo', methods=['POST'])
def search_videos():
    try:
        request_data = request.json
        url = request_data['url']

        file_path = download_youtube_video(url)
        if file_path and os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name='downloaded_video.mp4')
        else:
            return Response(json.dumps({"status": "error", "message": "Failed to download video"}), mimetype='application/json'), 500
    except Exception as e:
        return Response(json.dumps({"status": 0, "error_msg": str(e)}), mimetype='application/json'), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)