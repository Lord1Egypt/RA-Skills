# Domain model

This is the lean normalized model behind the skill.
Use it conceptually; do not dump schema jargon into user replies.

## Core entities

### Event
A scheduled race.
Key ideas:
- provider id
- track or course
- race number
- scheduled off time
- status

### Runner
A horse in an event.
Useful fields:
- horse name
- draw or barrier
- jockey
- trainer
- scratched status

### Market
A betting market for an event.
For v1, think mainly in terms of:
- win
- place

### Selection
A runner within a market.

### OddsQuote
A captured price for a selection.
In source-A-only v1, odds may be limited or absent, so do not assume they exist.

### Recommendation
A conversational judgment about a runner or selection.
Useful pieces:
- selection
- confidence
- reasons
- action type such as watch, paper, or approval-needed

## v1 simplification

For the current skill version, the practical object model is:
- race
- runners
- race conditions
- short verbal ranking

Keep user-facing output in those terms.
