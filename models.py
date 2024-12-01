from database import db
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'steps': self.steps,
            'prep_time': self.prep_time
        }

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    comment_text = db.Column(db.String(1000), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'comment_text': self.comment_text
        }
