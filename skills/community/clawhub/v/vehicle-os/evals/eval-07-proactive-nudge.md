# Eval 07: Proactive Nudge

## Setup Context
Subaru cabin filter overdue by 22,000 miles. Insurance renews in 45 days. User is logging a boat service.

## Input
"Did the spring commissioning on the boat today. Flushed the engine, charged the battery, checked all the electronics. Everything looks good."

## Expected Behavior
1. Logs boat service: spring commissioning, today, DIY, details
2. Updates boat maintenance record (commissioning done, next due spring 2027)
3. Confirms what was logged
4. Appends ONE nudge about the most urgent item across all vehicles (Subaru cabin filter overdue by 22K miles is more urgent than insurance in 45 days)

## What to Watch For
- Does the nudge cross vehicles (nudging about Subaru while logging boat work)?
- Does it pick the most urgent item?
- Is it a single line?
