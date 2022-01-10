from flask import Flask, render_template, Response
from cv2 import cv2

app = Flask(__name__)


@app.route('/')
def camera():
    return render_template('camera.html')


def get_frame():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    c = 0

    while True:
        ret, img = cam.read()
        if c % 8 == 0:
            cv2.imwrite("{}.jpg".format(c), img)
        c += 1
        imageCode = cv2.imencode('.jpg', img)[1]
        strData = imageCode.tostring()

        yield (b'--frame\r\n'
               b'Content-Type: Text/plain\r\n\r\n' + strData + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
