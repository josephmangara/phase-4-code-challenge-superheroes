from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-heropowers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    super_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero')

    def __repr__(self):
         return f"Name: {self.name}, Super Name: {self.super_name}"
    
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-heropowers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    power_heroes = db.relationship('HeroPower', backref='power')

    @validates('description')
    def validate_strength(self, key, value):
        if not value or len(value) < 10:
            raise ValueError("missing strength field or uncharacteristically short value.")
        return value 
    
    def __repr__(self):
         return f"Name: {self.name}, Description: {self.description}"

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropowers'

    serialize_rules = ('-hero.heropowers', '-power.heropowers',)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('strength')
    def validate_strength(self, key, value):
        if not value or len(value) < 4:
            raise ValueError("missing strength field or uncharacteristically short value.")
        return value 

    def __repr__(self):
        return f"Strength: {self.strength}, Hero ID: {self.hero_id}, Power ID: {self.power_id}"
