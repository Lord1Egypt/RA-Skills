# Eval 01: Add a New Vehicle

## Input
"I have a 2019 Subaru Outback Premium. Blue, about 67,000 miles. We call it the Subaru. I use synthetic oil."

## Expected Behavior
1. Creates vehicle profile with all provided details
2. Auto-suggests maintenance schedule adjusted for synthetic oil (7,500 mile oil change interval, not 5,000)
3. Presents the schedule as adjustable defaults
4. Asks about registration, insurance, and inspection info
5. Writes to vehicle-data.json

## What to Watch For
- Does it adjust the oil interval for synthetic?
- Does it capture the nickname?
- Does it present the schedule as customizable?
