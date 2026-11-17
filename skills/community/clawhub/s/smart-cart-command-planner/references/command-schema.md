# Command plan schema

Read this file whenever generating or reviewing a cart motion plan.

## Top-level object

```json
{
  "plan_version": "1.0",
  "status": "ready | needs_confirmation | emergency_stop",
  "request": {
    "original": "user request",
    "normalized_goal": "short normalized goal"
  },
  "assumptions": ["explicit assumption"],
  "steps": [],
  "safety": {
    "obstacle_check": true,
    "final_stop": true,
    "notes": ["safety note"]
  }
}
```

## Step object

Every step must contain:

- `seq`: positive integer starting at 1 with no gaps.
- `action`: one allowed action.
- `reason`: short explanation.

Allowed actions and fields:

| Action | Required fields | Limits |
| --- | --- | --- |
| `sense` | `clearance_required_cm` | 20-200 cm |
| `move_forward` | `distance_cm`, `speed` | 1-300 cm per step |
| `move_backward` | `distance_cm`, `speed` | 1-100 cm per step |
| `strafe_left` | `distance_cm`, `speed` | 1-150 cm per step |
| `strafe_right` | `distance_cm`, `speed` | 1-150 cm per step |
| `turn_left` | `angle_deg`, `speed` | 1-180 degrees |
| `turn_right` | `angle_deg`, `speed` | 1-180 degrees |
| `wait` | `duration_s` | 0.1-10 seconds |
| `stop` | none | must be final |

Use only `slow` or `medium` for `speed`. Treat `slow` as the default.

## Planning rules

1. Insert `sense` before the first movement unless the request is only `stop`.
2. Insert a new `sense` after every turn and before entering an uncertain segment.
3. Split movement longer than the per-step limit and insert `sense` between segments.
4. End every ordinary plan with `stop`.
5. Set `status` to `needs_confirmation` when the goal cannot be safely localized.
6. For emergency stop, return exactly one `stop` step and set `status` to `emergency_stop`.

