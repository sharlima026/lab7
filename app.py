from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab7.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True # use false for production
db = SQLAlchemy(app)

@app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)

# When the Flask app is shutting down, close the database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


from lab7.models import Pokemon

@app.route("/")
def hello():
    records = Pokemon.query.order_by(Pokemon.name.asc()).all()
    return render_template('index.html', pokemon=records)

# The args support the url queries request /pokemon?limit=12&offset=1
@app.route('/pokemon', methods=['GET'])
def show_all_pokemon():
    query = Pokemon.query.order_by(Pokemon.name.asc())
    start = request.args.get('offset', default=1, type=int)
    num_records = request.args.get('limit', default=10, type=int)
    records = query.paginate(start, num_records).items
    records = list(map(lambda x: x.toDict(), records))
    response = jsonify(records)
    return response

@app.route('/pokemon/type1', methods=['GET'])
def get_all_pokemon_type():
    #https://docs.sqlalchemy.org/en/latest/orm/query.html#distinct
    records = db.session.query(Pokemon.type_1).distinct().all()
    records = list(map(lambda x: x[0], records))
    response = jsonify(records)
    return response

@app.route('/pokemon/type1/<type_1>', methods=['GET'])
def get_pokemon_by_type(type_1):
    records = Pokemon.query.filter_by(type_1=type_1)
    records = [rec.toDict() for rec in records]
    response = jsonify(records)
    return response


@app.route('/pokemon/<pk_id>')
def get_pokemon_by_id(pk_id):
    pokemon = Pokemon.query.get(pk_id)
    return render_template('detail.html', pokemon=pokemon)