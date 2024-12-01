from flask import Flask, jsonify, request
from models import Recipe, Rating, Comment
from sqlalchemy.exc import SQLAlchemyError
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:InvinithExam!@db:1433/RecipesDB?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)

@app.route('/')
def home():
    return "Invinith Exam"

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    try:
        new_recipe = Recipe(
            name=data['name'],
            ingredients=data['ingredients'],
            steps=data['steps'],
            prep_time=data['prep_time']
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({"message": "Recipe added successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()  # Sort by most recent
        return jsonify([recipe.to_dict() for recipe in recipes]), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 500

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    try:
        recipe = Recipe.query.get(id)
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404
        return jsonify(recipe.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 500

@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.get_json()
    try:
        recipe = Recipe.query.get(id)
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404

        # Update recipe fields
        recipe.name = data.get('name', recipe.name)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)
        recipe.steps = data.get('steps', recipe.steps)
        recipe.prep_time = data.get('prep_time', recipe.prep_time)

        db.session.commit()
        return jsonify({"message": "Recipe updated successfully!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        recipe = Recipe.query.get(id)
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404

        db.session.delete(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe deleted successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/recipes/<int:id>/ratings', methods=['POST'])
def add_rating(id):
    data = request.get_json()

    try:
        recipe = Recipe.query.get(id)
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404

        rating_value = data.get('rating')
        if rating_value < 1 or rating_value > 5:
            return jsonify({"message": "Rating must be between 1 and 5"}), 400

        new_rating = Rating(recipe_id=id, rating=rating_value)
        db.session.add(new_rating)
        db.session.commit()
        return jsonify({"message": "Rating added successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/recipes/<int:id>/comments', methods=['POST'])
def add_comment(id):
    data = request.get_json()

    try:
        recipe = Recipe.query.get(id)
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404

        comment_text = data.get('comment')
        if not comment_text:
            return jsonify({"message": "Comment cannot be empty"}), 400

        new_comment = Comment(recipe_id=id, comment_text=comment_text)
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({"message": "Comment added successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/recipes/<int:id>/comments', methods=['GET'])
def get_comments(id):
    try:
        recipe = Recipe.query.get(id)
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404

        comments = Comment.query.filter_by(recipe_id=id).all()

        # If no comments found, return an empty list
        return jsonify([comment.to_dict() for comment in comments]), 200

    except SQLAlchemyError as e:
        # Return a server error if the database query fails
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()  # Attempt to create the tables
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
    app.run(host='0.0.0.0', port=5000, debug=True)