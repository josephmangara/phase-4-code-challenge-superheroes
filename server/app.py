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
    heroes = [hero.to_dict() for hero in Hero.query.all()]
    return jsonify(heroes), 200

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()
    hero_dict = hero.to_dict()

    response = make_response(
        hero_dict,
        200
        )
    
    return response

    # hero = Hero.query.get(id)
    # if hero:
    #     return jsonify(hero.to_dict()), 200
    # else:
    #     return jsonify({"error": "Hero not found"}), 404

@app.route('/powers')
def powers():
    powers = []
    for power in Power.query.all():
        powers_dict = power.to_dict()
        powers.append(powers_dict)

    response = make_response(
        jsonify(powers),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555)
