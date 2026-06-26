# Eval 03: Multi-Vehicle Maintenance Check

## Setup Context
Two vehicles: Subaru (67,500 mi, cabin filter overdue, tire rotation due at next oil change) and a boat (spring commissioning due, impeller overdue).

## Input
"What maintenance is coming up?"

## Expected Behavior
1. Groups by vehicle
2. Shows overdue items clearly (cabin filter, impeller)
3. Shows upcoming items (tire rotation, spring commissioning)
4. Skips items that aren't due
5. Offers to mark things as done or schedule service

## What to Watch For
- Does it handle two different vehicle types (car vs. boat) with appropriate terminology?
- Does it distinguish overdue from upcoming?
- Is it scannable?
