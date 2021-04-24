import os
import json

from flask import Flask, request, url_for
from sqlalchemy import create_engine

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


def _create_connection():

    # engine = create_engine(config['DATABASE_URI'], echo=True)
    engine = create_engine("postgresql+psycopg2://myuser:passwd@192.168.49.2:31131/myapp", echo=True)
    return engine

@app.route('/db')
def db():

    engine = _create_connection()
    rows = []
    with engine.connect() as connection:
        result = connection.execute("select id, name from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# !добавить пользователя!
@app.route("/user", methods=['POST'])
def create_user():
    engine = _create_connection()
    _userid = request.json["id"]
    _name = request.json["name"]
    try:
        with engine.connect() as connection:
            result = connection.execute(f"insert into client(id, name) values ({_userid}, '{_name}');")
        return 'Пользователь добавлен.'
    except Exception as e:
        return f"{e.args}"


# !получить пользователя
@app.route("/user/<userid>", methods=['GET'])
def get_user(userid):
    engine = _create_connection()
    with engine.connect() as connection:
        result = connection.execute(f"select id, name from client where id={userid}")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# удалить пользователя
@app.route("/user/<userid>", methods=['DELETE'])
def delete_user(userid):
    engine = _create_connection()
    try:
        with engine.connect() as connection:
            result = connection.execute(f"DELETE FROM client WHERE id={userid}")
        return 'Пользователь удален.'
    except Exception as e:
        return f"{e.args}"



# обновить пользователя
@app.route("/user/<userid>", methods=['PUT'])
def update_user(userid):
    engine = _create_connection()
    _name = request.json["name"]
    try:
        with engine.connect() as connection:
            result = connection.execute(f"UPDATE client SET name='{_name}' WHERE id={userid}")
        return 'Данные пользователя обновлены.'
    except Exception as e:
        return f"{e.args}"

# Получить все записи по таблице client
@app.route("/users", methods=['GET'])
def all_clients():
    engine = _create_connection()
    try:
        with engine.connect() as connection:
            result = connection.execute(f"SELECT * FROM client ORDER BY id;")
            rows = [dict(r.items()) for r in result]
        return json.dumps(rows, sort_keys=True, indent=4)
    except Exception as e:
        return f"{e.args}"



if __name__ == "__main__":
    # print(str(create_user(1))+'1')
    app.run(host='0.0.0.0', port='8000', debug=True)
    # with app.test_request_context():
    #     print(url_for('get_user', userid = '1'))
    #     print(url_for('create_user'))