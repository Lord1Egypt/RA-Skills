# Reminder Policy

Skill Router should be quiet by default.

## Give a reminder when
- the task would likely benefit from a clearly relevant installed skill
- not reminding would likely cause repeated wasted work
- the user explicitly asked about skills
- the current task could easily go down the wrong tool path without a short routing hint
- there is no strong installed match and a clean discovery flow would save time

## Stay silent when
- the right skill is already obviously active
- the task is simple enough that a routing hint adds no value
- the user is already in the correct workflow
- mentioning skills would make the response heavier than the task itself

## Style
- short
- concrete
- one recommendation is usually enough
- mention a backup only if it materially changes the next step

## Rule
Skill Router should feel like a useful nudge, not a layer of bureaucracy.
