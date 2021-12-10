import flask
from database import all_users_list
app = flask.Flask('my_server')


@app.route('/', methods=['GET'])
def just_text():
    a = ''
    for x in all_users_list:
        a = a + str(x)
    return '<tt>' + a + '</tt> \n'


@app.route('/', methods=['POST'])
def post():
    name = flask.request.form["name"]
    all_users_list.append(name)


app.run()
