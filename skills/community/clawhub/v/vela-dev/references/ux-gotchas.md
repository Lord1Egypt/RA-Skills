# UX Gotchas

## Template/event constraints

### Unsupported event pattern
This kind of expression can fail:
- `onclick="goView('" + ($item.v) + "')"`

A known error looks like:
- `Unsupported Event value: "goView('" + ($item.v) + "')"`

Prefer one of these forms instead:
1. direct function name
2. normal call expression like `funName(x, y)` if supported in context
3. simpler static handlers

When dynamic list behavior is needed, prefer index-based handlers or explicit per-item handlers over complex template concatenation.

## CSS parsing failures

A broken or orphaned CSS block may produce:
- `Error: loader error: UxLoader`
- `### Css ### Unexpected }`

Checklist:
- inspect the style block near the reported line
- look for missing selector names
- look for duplicated or stray `}`
- patch the smallest broken region first

## Build workflow

Useful commands:
- `cd <project> && npx aiot build`
- `cd <project> && npx aiot build 2>&1 | grep -E "success|error|Error"`
- `cd <project> && npx aiot build 2>&1 | grep -E "error|Error|:" | tail -20`

## Layout advice

- If a home page needs scrolling, prefer `list`
- Avoid assuming web-style scrolling containers behave the same way
- Test the simplest reliable Vela component first
