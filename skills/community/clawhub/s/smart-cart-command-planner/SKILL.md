---
name: smart-cart-command-planner
description: Convert Chinese or English natural-language requests for an OpenClaw-powered omnidirectional smart cart into conservative, structured motion plans. Use for command understanding, task decomposition, waypoint planning, obstacle-aware movement, emergency-stop handling, and JSON control-plan generation for carts that support forward, backward, lateral movement, turning, sensing, waiting, and stopping.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🛒"
---

# Smart Cart Command Planner

Convert a user's movement request into a safe plan. Produce a plan for a downstream controller; do not claim that the cart has executed any action.

## Workflow

1. Parse the request into destination, direction, distance, angle, speed, stopping condition, and obstacle constraints.
2. Identify missing information that changes safety or feasibility. Ask a focused question when a destination, route, or unit is essential. Otherwise record a conservative assumption.
3. Read [references/command-schema.md](references/command-schema.md) before producing the plan.
4. Decompose the request into only the allowed actions in the schema.
5. Insert `sense` before motion when obstacle clearance is unknown and insert `stop` as the final step.
6. Use `slow` speed near obstacles, people, turns, narrow areas, or uncertain routes.
7. Return one JSON object followed by a short human-readable explanation.
8. Save the JSON to a file and run `python3 scripts/validate_plan.py PLAN.json` when file execution is available. Fix every reported error before presenting the plan.

## Safety Rules

- Prioritize an explicit emergency-stop request over all other instructions. Return a single `stop` step and mark the plan `emergency_stop`.
- Never invent live sensor readings, coordinates, clearances, successful execution, or a connection to hardware.
- Never bypass collision checks or continue motion after a sensor, controller, or communication fault.
- Keep each movement segment within the limits defined in the schema. Split long movement into multiple segments separated by `sense`.
- Use `needs_confirmation` when the user requests high speed, an unclear destination, movement around people, or a route without observable clearance.
- Preserve the user's units in `request.original`; normalize distance to centimeters and angles to degrees in the steps.

## Output Quality

- Make every step executable and ordered.
- State assumptions explicitly instead of hiding uncertainty.
- Include a measurable completion condition for every movement step.
- Keep explanations concise and separate from the machine-readable JSON.

## Example

For `向前移动1米，右转90度，再前进50厘米并停下`, produce steps for sensing, moving forward 100 cm, turning right 90 degrees, sensing again, moving forward 50 cm, and stopping. See [examples/sample-plan.json](examples/sample-plan.json).

