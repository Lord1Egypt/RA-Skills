# Digest templates

Keep digests short, scannable, and channel-safe (avoid tables by default).

## Daily digest (example)

**Wellness — {date}**

- Sleep: {sleep.duration_minutes} min (score {sleep.score})
- Recovery: {recovery.score} | HRV {recovery.hrv_ms} ms | RHR {recovery.resting_hr_bpm} bpm
- Activity: {activity.steps} steps | {activity.distance_km} km
- Training: {training.workouts_count} workouts | top strain {training.top_strain}
- Weight: {body.weight_kg} kg

## Weekly digest (example)

**Wellness — week of {start_date}**

- Avg sleep: {avg_sleep_hours} h
- Avg recovery: {avg_recovery}
- Total workouts: {workout_count}
- Total distance: {total_distance_km} km
- Weight trend: {delta_weight_kg} kg

## Channel formatting

- discord: allow **bold**
- slack/whatsapp: prefer *bold*
- telegram: prefer plain text
