from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
db = SQLAlchemy(app)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)

    def __init__(self, path):
        self.path = path


@app.route('/', methods=['POST', 'GET'])
def request_function():
    if request.method == 'POST':
        try:
            cap = cv2.VideoCapture(0)
            for i in range(10):
                cap.read()
            ret, frame = cap.read()
            path = 'pictures/'+str(datetime.utcnow()) + '.png'
            path = path.replace(' ', '_')
            cv2.imwrite('static/'+path, frame)
            cap.release()
            new_picture = Media(path)
            db.session.add(new_picture)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        pictures = Media.query.all()
        return render_template('index.html', pictures=pictures)


if __name__ == '__main__':
    app.run()
