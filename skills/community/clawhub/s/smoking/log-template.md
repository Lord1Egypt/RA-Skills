# Logging Template and Metrics

Use this template to keep events consistent and analyzable.

## Event Template

```text
HH:MM | product | amount | trigger | location | intensity(1-10) | response_used | notes
```

Example:

```text
08:40 | cigarette | 1 | commute stress | outside office | 7 | delayed 10 min | still smoked after call
```

## Minimum Fields

- time
- product and amount
- trigger label
- intensity score 1 to 10

Optional but useful:
- location
- response used
- social context

## Weekly Metrics

Track these every 7 days:

- total events per day average
- first-use time trend
- top trigger share (percent)
- response success rate
- longest smoke-free window

## Interpretation Guide

- event count down with same trigger profile -> progress in quantity
- trigger share down for one context -> local intervention is working
- intensity down before event count moves -> early stabilization stage
- no movement for 2 weeks -> change one variable, not all variables
