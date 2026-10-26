from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(["strength", "cardio", "core", "flexibility"]),
    )
    equipment_needed = fields.Bool()


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def require_one_measure(self, data, **kwargs):
        if not any(k in data for k in ("reps", "sets", "duration_seconds")):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str()
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)
