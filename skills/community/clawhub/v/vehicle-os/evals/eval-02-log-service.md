# Eval 02: Log Service with Mechanic Note

## Input
"Got the oil changed on the Subaru today at Main Street Auto. 67,500 miles, $85. They said front brakes are at about 40%."

## Expected Behavior
1. Logs the service with all details (oil change, 67,500 mi, Main Street Auto, $85)
2. Adds Main Street Auto to mechanic directory if not there
3. Updates next oil change due date/mileage
4. Captures the 40% brake note and sets a future brake inspection flag
5. Estimates brake life remaining and tells the user

## What to Watch For
- Does it calculate the next oil change correctly?
- Does it proactively handle the brake warning (not just log it, but project when action is needed)?
- Does it auto-add the mechanic to the directory?
