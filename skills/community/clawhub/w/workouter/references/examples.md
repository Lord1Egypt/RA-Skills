# Worked examples

Each example shows the request, the confirmation summary to show the user, and the `create_workout` input. Examples use sample paces and loads. Never reuse a number the user did not give you.

## 1. Steady run

Request: "Build me a 30 minute easy run."

Summary: **30 Minute Easy Run**, outdoor run. 30 min, no target.

```json
{
  "workoutType": "singleGoalWorkout",
  "activityType": "running",
  "location": "outdoor",
  "displayName": "30 Minute Easy Run",
  "swimmingLocation": "",
  "goal": { "type": "time", "targetDuration": 1800, "unit": "seconds" }
}
```

## 2. Timed intervals

Request: "40 minute interval run: 10 minute warmup, 5 x 3 minutes hard with 2 minutes easy, then a 5 minute cooldown."

Summary: **5 x 3 Minute Intervals**, outdoor run. Warmup 10 min, then 5 times (3 min hard, 2 min easy), cooldown 5 min.

```json
{
  "workoutType": "customWorkout",
  "activityType": "running",
  "location": "outdoor",
  "displayName": "5 x 3 Minute Intervals",
  "swimmingLocation": "",
  "warmup": {
    "goal": { "type": "time", "targetDuration": 600, "unit": "seconds" },
    "displayName": "Easy warmup"
  },
  "blocks": [
    {
      "iterations": 5,
      "steps": [
        { "purpose": "work", "goal": { "type": "time", "targetDuration": 180, "unit": "seconds" }, "displayName": "Hard" },
        { "purpose": "recovery", "goal": { "type": "time", "targetDuration": 120, "unit": "seconds" }, "displayName": "Easy" }
      ]
    }
  ],
  "cooldown": {
    "goal": { "type": "time", "targetDuration": 300, "unit": "seconds" },
    "displayName": "Easy cooldown"
  }
}
```

## 3. Distance repeats with a pace target

Request: "6 x 800 m at 5K pace with 2 minute jogs. My 5K pace is 4:30 per km."

Convert the pace: 4:30 per km is 270 seconds per km, so 3600 / 270 = 13.3 km/h. Use a narrow range around it and say so in the summary.

Summary: **6 x 800 m at 5K Pace**, outdoor run. Warmup 10 min, then 6 times (800 m at about 4:30 per km, 2 min jog), cooldown 10 min.

```json
{
  "workoutType": "customWorkout",
  "activityType": "running",
  "location": "outdoor",
  "displayName": "6 x 800 m at 5K Pace",
  "swimmingLocation": "",
  "warmup": { "goal": { "type": "time", "targetDuration": 600, "unit": "seconds" } },
  "blocks": [
    {
      "iterations": 6,
      "steps": [
        {
          "purpose": "work",
          "goal": { "type": "distance", "targetValue": 800, "unit": "meters" },
          "alert": { "type": "speedRange", "lowerBound": 13.0, "upperBound": 13.7, "unitSpeed": "kilometersPerHour" },
          "displayName": "800 m"
        },
        { "purpose": "recovery", "goal": { "type": "time", "targetDuration": 120, "unit": "seconds" }, "displayName": "Jog" }
      ]
    }
  ],
  "cooldown": { "goal": { "type": "time", "targetDuration": 600, "unit": "seconds" } }
}
```

## 4. Gym straight sets

Request: "Barbell rows 3 x 10 at 40 kg, then overhead press 3 x 8 at 25 kg, 90 seconds rest."

Tell the user the watch shows timed steps, with the exercise, reps and load in each step's name.

Summary: **Back and Shoulders**, indoor strength. Barbell row 3 x 10 at 40 kg, overhead press 3 x 8 at 25 kg, 90 s rest between sets.

```json
{
  "workoutType": "customWorkout",
  "activityType": "traditionalStrengthTraining",
  "location": "indoor",
  "displayName": "Back and Shoulders",
  "swimmingLocation": "",
  "blocks": [
    {
      "iterations": 3,
      "steps": [
        { "purpose": "work", "goal": { "type": "time", "targetDuration": 60, "unit": "seconds" }, "displayName": "Barbell row, 10 reps, 40 kg" },
        { "purpose": "recovery", "goal": { "type": "time", "targetDuration": 90, "unit": "seconds" }, "displayName": "Rest" }
      ]
    },
    {
      "iterations": 3,
      "steps": [
        { "purpose": "work", "goal": { "type": "time", "targetDuration": 60, "unit": "seconds" }, "displayName": "Overhead press, 8 reps, 25 kg" },
        { "purpose": "recovery", "goal": { "type": "time", "targetDuration": 90, "unit": "seconds" }, "displayName": "Rest" }
      ]
    }
  ]
}
```

## 5. Pool swim with send-off times

Request: "Pool swim: 200 warmup, 4 x 100 freestyle on 1:45, 100 cooldown."

Summary: **Pool Send-Off Set**, pool swim. Warmup 200 m, then 4 times 100 m on 1:45, cooldown 100 m.

```json
{
  "workoutType": "customWorkout",
  "activityType": "swimming",
  "location": "indoor",
  "displayName": "Pool Send-Off Set",
  "swimmingLocation": "pool",
  "warmup": { "goal": { "type": "distance", "targetValue": 200, "unit": "meters" } },
  "blocks": [
    {
      "iterations": 4,
      "steps": [
        {
          "purpose": "work",
          "goal": { "type": "distanceAndDuration", "targetDistance": 100, "distanceUnit": "meters", "targetDuration": 105 },
          "displayName": "Freestyle"
        }
      ]
    }
  ],
  "cooldown": { "goal": { "type": "distance", "targetValue": 100, "unit": "meters" } }
}
```

## 6. Open session

Request: "Just an open stretching session."

```json
{
  "workoutType": "singleGoalWorkout",
  "activityType": "yoga",
  "location": "indoor",
  "displayName": "Stretching",
  "swimmingLocation": "",
  "goal": { "type": "open" }
}
```
