# FitnessTracker Schema

Complete data structure definition for exercise and fitness tracking.

## Field Quick Reference

### Core Fields

| Field | Type | Description |
|-----|------|-------------|
| `workout_records` | array | Workout records |
| `fitness_goals` | array | Fitness goals |
| `statistics` | object | Statistics data |
| `body_composition` | object | Body composition records |
| `prescriptions` | object | Exercise prescription reference |

## workout_records Array Item

| Field | Type | Description |
|-----|------|-------------|
| `date` | string | Workout date |
| `time` | string | Workout time (HH:mm) |
| `type` | enum | Workout type |
| `duration_minutes` | number | Duration (minutes) |
| `intensity` | object | Workout intensity |
| `heart_rate` | object | Heart rate data |
| `distance_km` | number | Distance (kilometers) |
| `pace_min_per_km` | string | Pace |
| `calories_burned` | number | Calories burned |
| `how_felt` | enum | Subjective feeling |
| `notes` | string | Notes |

## type Enum Values

### Aerobic Exercise
- running (Running), walking (Brisk walking)
- cycling (Cycling), swimming (Swimming)
- jump_rope (Jump rope), aerobics (Aerobics)
- elliptical (Elliptical), rowing (Rowing machine)

### Strength Training
- strength (Strength)
- calisthenics (Bodyweight training)
- machine_weights (Machine weights)
- free_weights (Free weights)
- resistance_bands (Resistance bands)

### Sports
- basketball (Basketball), soccer (Soccer)
- badminton (Badminton), ping_pong (Table tennis)
- tennis (Tennis), volleyball (Volleyball)

### Other Activities
- yoga (Yoga), pilates (Pilates)
- tai_chi (Tai Chi), dance (Dance)
- hiking (Hiking), skiing (Skiing)

## intensity Object

| Field | Type | Description |
|-----|------|-------------|
| `level` | enum | low/moderate/high |
| `rpe` | integer | RPE 6-20 |

### RPE Reference
- 6-8: Very easy
- 9-11: Very easy
- 12-14: Somewhat hard
- 15-17: Hard
- 18-20: Very hard

## fitness_goals Array Item

| Field | Type | Description |
|-----|------|-------------|
| `goal_id` | string | Goal ID |
| `category` | enum | Goal category |
| `title` | string | Goal title |
| `start_date` | string | Start date |
| `target_date` | string | Target date |
| `baseline_value` | number | Baseline value |
| `current_value` | number | Current value |
| `target_value` | number | Target value |
| `unit` | string | Unit |
| `progress` | number | Progress percentage |
| `status` | enum | Status |

## category Enum Values

- weight_loss (Weight loss goal)
- muscle_gain (Muscle gain goal)
- endurance (Endurance goal)
- health (Health goal)
- habit (Habit formation)

## statistics Object

| Field | Type | Description |
|-----|------|-------------|
| `total_workouts` | int | Total workout count |
| `total_duration_minutes` | number | Total duration (minutes) |
| `total_distance_km` | number | Total distance (kilometers) |
| `total_calories_burned` | number | Total calories burned |
| `current_streak_days` | int | Current streak days |
| `longest_streak_days` | int | Longest streak days |

## Data Storage

- Location: `data/fitness-tracker.json`
