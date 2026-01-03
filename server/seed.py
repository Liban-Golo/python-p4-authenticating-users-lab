# server/seed.py
from app import app
from models import db, User

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(username="Liban"),
        User(username="Alice"),
        User(username="Bob")
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Seeded database with users!")
