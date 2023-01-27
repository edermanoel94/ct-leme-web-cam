from flask import Flask, Response, jsonify, make_response

from video import Video

app = Flask(__name__)


@app.route('/health')
def health():
    return make_response(jsonify(status="OK"), 200)


@app.route('/')
def show():
    return Response(frame_to_img(Video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def frame_to_img(video):
    while True:
        frame = video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame
               + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
