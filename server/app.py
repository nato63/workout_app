from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
we_schema = WorkoutExerciseSchema()


# ---------- Workouts ----------
@app.get("/")
def index():
    return jsonify({"message": "Welcome to the Workout API!"}), 200


@app.get("/workouts")
def get_workouts():
    return jsonify(WorkoutSchema(many=True).dump(Workout.query.all())), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except (ValidationError, ValueError) as e:
        db.session.rollback()
        return jsonify({"errors": getattr(e, "messages", str(e))}), 400
    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204


# ---------- Exercises ----------
@app.get("/exercises")
def get_exercises():
    return jsonify(ExerciseSchema(many=True).dump(Exercise.query.all())), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except (ValidationError, ValueError) as e:
        db.session.rollback()
        return jsonify({"errors": getattr(e, "messages", str(e))}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create exercise (duplicate name?)"}), 400
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204


# ---------- Add exercise to workout ----------
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    if not db.session.get(Workout, workout_id) or not db.session.get(
        Exercise, exercise_id
    ):
        return jsonify({"error": "Workout or exercise not found"}), 404
    try:
        data = we_schema.load(request.get_json())
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(we)
        db.session.commit()
    except (ValidationError, ValueError) as e:
        db.session.rollback()
        return jsonify({"errors": getattr(e, "messages", str(e))}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Exercise already in this workout"}), 400
    return jsonify(we_schema.dump(we)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
