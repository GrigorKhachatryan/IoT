import psycopg2
import psycopg2.extras
from flask import Flask, render_template,request

app = Flask(__name__)

connection = psycopg2.connect(user="postgres",
                              password="йцу1024кен",
                              host="localhost",
                              port="5434",
                              database="Camera")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


@app.route("/up/iot", methods=['GET'])
def information():
    message = request.args.get('message')
    camera = request.args.get('camera')
    dates = request.args.get('date')
    cursor.execute('insert into Statistics (message,Camera_name, dates) values (%s,%s,%s)', (message, camera, dates))
    connection.commit()
    return 'ok'


@app.route("/iot", methods=['GET'])
def info():
    camera = request.args.get('camera')
    if camera is None:
        cursor.execute('select message, Camera_name, dates from Statistics')
    else:
        cursor.execute('select message, Camera_name, dates from Statistics where Camera_name=%s',(camera,))
    data = cursor.fetchall()
    cursor.execute('select * from Camera')
    camera = cursor.fetchall()
    return render_template('index.html', mes=data, cam=camera)


@app.route("/сamera", methods=['GET'])
def cameras():
    return render_template('camera.html')

@app.route("/sign", methods=['GET'])
def cameras():
    return render_template('sign.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0')