#!/usr/bin/env python3

from app import app, db
from models import Hero, Power, HeroPower
import random 
from sqlalchemy import func 

with app.app_context():
    # Delete existing data
    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()

    # Powers
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for power_info in powers_data:
        power = Power(**power_info)
        db.session.add(power)

    #  Heroes
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for hero_info in heroes_data:
        hero = Hero(**hero_info)
        db.session.add(hero)

    
    db.session.commit()

    # Adding Powers to Heroes
    strengths = ["Strong", "Weak", "Average"]

    for hero in Hero.query.all():
        for _ in range(random.randint(1, 3)):
            power = Power.query.order_by(func.random()).first()  # Randomly select a power
            hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=random.choice(strengths))
            db.session.add(hero_power)

   
    db.session.commit()

   
