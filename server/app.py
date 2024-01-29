from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the superheroes API"})

@app.route('/heroes', methods=['GET'])
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'created_at': hero.created_at,
            'updated_at': hero.updated_at,
            'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description, 'strength': hp.strength} for hp in hero.hero_powers]
        }
        heroes.append(hero_dict)

    return jsonify(heroes), 200

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()
    if hero:
        hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'created_at': hero.created_at,
            'updated_at': hero.updated_at,
            'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description, 'strength': hp.strength} for hp in hero.hero_powers]
        }
        return jsonify(hero_dict), 200
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers')
def powers():
    powers = []
    for power in Power.query.all():
        power_dict = {
            'id': power.id,
            'name': power.name,
            'description': power.description,
            'created_at': power.created_at,
            'updated_at': power.updated_at,
            'heroes': [{'id': hp.hero.id, 'name': hp.hero.name, 'super_name': hp.hero.super_name, 'strength': hp.strength} for hp in power.power_heroes]
        }
        powers.append(power_dict)

    return jsonify(powers), 200



if __name__ == '__main__':
    app.run(port=5555)
