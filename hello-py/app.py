import os
import json

from flask import Flask, url_for

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': 'HostName', #os.environ['HOSTNAME'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}

@app.route("/health")
def health():
    return '{"status": "ok"}'


@app.route("/version")
def version():
    return '{"version": "1"}'


@app.route("/")
def hello():
    return 'Hello world!!!' #from '+ os.environ['HOSTNAME'] + '!'

@app.route("/user", methods=['POST'])
def create_user():
    return 'user create' #from '+ os.environ['HOSTNAME'] + '!'

@app.route("/user/<userid>")
def get_user(userid):
    return 'user ' + userid  #from '+ os.environ['HOSTNAME'] + '!'

@app.route('/db')
def db():
    from sqlalchemy import create_engine

    # engine = create_engine('postgresql+psycopg2://myuser:passwd@postgres/myapp', echo=True)
    engine = create_engine(config['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = connection.execute("select id, name from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)


if __name__ == "__main__":
    # print(db())
    app.run(host='0.0.0.0', port='80', debug=True)
    # with app.test_request_context():
    #     print(url_for('get_user', userid = '1'))
    #     print(url_for('create_user'))