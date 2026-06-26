# Eval 05: Cost Tracking and Summary

## Setup Context
Subaru service history: oil change $85 (Jan), tire rotation $40 (Jan), brake pads $320 (March), cabin filter $25 (March, DIY). Boat: impeller $150 (April).

## Input
"How much have I spent on vehicles this year?"

## Expected Behavior
1. Groups by vehicle
2. Shows line items with dates and costs
3. Shows per-vehicle totals
4. Shows grand total
5. Notes the DIY item had a parts cost but no labor
6. Could show cost-per-mile for the Subaru if mileage data supports it

## What to Watch For
- Does it group by vehicle correctly?
- Does it handle the DIY item (cost but no mechanic)?
- Is the math correct?
- Does it include visit/service counts alongside totals?
