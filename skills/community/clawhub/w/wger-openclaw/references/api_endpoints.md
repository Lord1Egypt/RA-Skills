# wger API Endpoints Reference

## Authentication
- Header: Authorization: Token [your_token]
- Base: https://wger.de/api/v2/

## Workouts & Logs
- List routines: GET /workout/?format=json&limit=10
- Create log: POST /workoutlog/ {date, workout, exercises[]}
- View log: GET /workoutlog/[id]/ {reps, weight, date}
- Update log: PATCH /workoutlog/[id]/ 

## Nutrition
- Log meal: POST /nutritionlog/ {date, meal_id, nutritional_values {calories, protein}}
- Goals: GET /weight/ for weight logs

## Exercises
- Search: GET /exercise/?search=squat&language=2 (EN)

Full docs: https://wger.readthedocs.io/en/latest/api.html
