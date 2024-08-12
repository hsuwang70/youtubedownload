import yt_dlp
from flask import Flask, request, Response
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
request_methods = ["POST"]

def get_temp_folder():
    # 獲取臨時目錄
    return tempfile.gettempdir()

def download_youtube(request_data):
    url = request_data['url']
    download_folder = get_temp_folder()
    print(f"Download folder: {download_folder}")

    output_template = os.path.join(download_folder, 'downloaded_video.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return {"status": 1, "message": "Download successful"}
    except Exception as e:
        return {"status": 0, "error_msg": str(e)}

@app.route('/downloadyoutube', methods=['POST'])
def get_report():
    try:
        request_data = request.json
        result = download_youtube(request_data)
        return Response(json.dumps(result), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"status": 0, "error_msg": str(e)}), mimetype='application/json'), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)