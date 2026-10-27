# Workout Tracker API

## Description

A backend REST API for a workout tracking application used by personal trainers. It is built with Flask, SQLAlchemy, Flask-Migrate and Marshmallow.

The API tracks **workouts** and the **exercises** inside them. Exercises are reusable, so the same exercise (for example "Squat") can be added to many different workouts. Each exercise inside a workout stores its own sets, reps, or duration.

### Models

- **Exercise**: `name`, `category`, `equipment_needed`
- **Workout**: `date`, `duration_minutes`, `notes`
- **WorkoutExercise** (join table): `workout_id`, `exercise_id`, `sets`, `reps`, `duration_seconds`

### Relationships

- A Workout has many WorkoutExercises.
- An Exercise has many WorkoutExercises.
- Workouts and Exercises are many-to-many through WorkoutExercise.

### Validations

- **Table constraints:** workout duration must be greater than 0, sets/reps/duration cannot be negative, and an exercise can only be added to a workout once.
- **Model validations:** exercise names need at least 2 characters, workout duration must be positive, and sets/reps/duration cannot be negative.
- **Schema validations:** category must be one of `strength`, `cardio`, `core`, `flexibility`, numeric fields must be in range, and a workout exercise needs at least one of `reps`, `sets`, or `duration_seconds`.

## Installation

Requires Python 3.11 and [Pipenv](https://pipenv.pypa.io/).

1. Clone the repository and move into it:

   ```
   git clone <your-repo-url>
   cd workout_app
   ```

2. Install the dependencies:

   ```
   pipenv install
   ```

3. Activate the virtual environment:

   ```
   pipenv shell
   ```

4. Move into the server folder:

   ```
   cd server
   ```

5. Create the database tables from the existing migrations:

   ```
   export FLASK_APP=app.py
   flask db upgrade
   ```

6. Seed the database with example data:
   ```
   python seed.py
   ```

## Running the app

From the `server` folder, with the environment active:

```
flask run
```

The API runs at `http://127.0.0.1:5000`.

To reload automatically when you edit code, use `flask run --debug`.

## Endpoints

### Workouts

- `GET /` : welcome message
- `GET /workouts` : list all workouts with their exercises
- `GET /workouts/<id>` : get one workout (404 if not found)
- `POST /workouts` : create a workout
- `DELETE /workouts/<id>` : delete a workout

### Exercises

- `GET /exercises` : list all exercises
- `GET /exercises/<id>` : get one exercise (404 if not found)
- `POST /exercises` : create an exercise
- `DELETE /exercises/<id>` : delete an exercise

### Workout exercises

- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` : add an exercise to a workout with sets, reps, or duration

### Example request bodies

Create a workout (`POST /workouts`):

```json
{
  "date": "2026-10-27",
  "duration_minutes": 45,
  "notes": "Leg day"
}
```

Create an exercise (`POST /exercises`):

```json
{
  "name": "Lunge",
  "category": "strength",
  "equipment_needed": false
}
```

Add an exercise to a workout (`POST /workouts/1/exercises/2/workout_exercises`):

```json
{
  "sets": 3,
  "reps": 12
}
```

### Error responses

- `400`: invalid data (the response lists the validation errors)
- `404`: workout or exercise not found

## Project structure

```
workout_app/
├── Pipfile
├── README.md
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    └── migrations/
```
