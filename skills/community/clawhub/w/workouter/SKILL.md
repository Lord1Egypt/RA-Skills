---
name: build-workout
description: Build a structured workout and send it to the user's Apple Watch with the Workouter MCP tools. Use when the user wants to create, plan, or send a run, ride, swim, walk, hike, row, elliptical, strength, HIIT, EMOM, circuit, or interval workout to their watch, or asks for "a workout" they can follow on their wrist.
---

# Build a Workouter workout

The Workouter MCP server (`workouter`) turns a structured workout into an
Apple WorkoutKit file and delivers it to the user's Apple Watch. There is
no Garmin support. Don't offer another device, and if the user asks for one,
say it isn't available.

The workout shape is `create_workout`'s `inputSchema`. It is the source of
truth, so read it for field names and enums. This skill covers what the
schema can't tell you: when to ask a question, and how to map real workouts
onto WorkoutKit's limited primitives.

## 1. Check before building

Call `get_delivery_status` and `get_quota` first (they are independent, so
call them together):

- If either returns `subscription_required`, stop. Every Workouter tool call
  requires Pro. Relay the message and `upgrade_url`, then stop and wait for
  the user. Don't retry.
- If `remaining` is 0, say the weekly limit is reached and stop.
- If `can_auto_push` is false, tell the user up front that they'll get a
  link to open on their phone instead of an automatic push to the watch.

## 2. Never make up missing details

Ask the user instead of guessing when any of these are missing:

- **Units.** "Run 5" has no unit, so ask. "5k", "5 miles", and "run for 5"
  (minutes) are clear.
- **Grouping.** "Some hard intervals" has no count and no per-rep length, so
  ask. "6x1 min hard, 1 min easy" is clear.
- **Pool units.** For swims, use exactly the meters or yards the user gave,
  and never convert. Ask if they didn't say.

When recovery isn't mentioned, time intervals get equal recovery time and
distance intervals get half-distance recovery. Tell the user you did this.

Some requests are precise but can't be done. Say so, and suggest an
alternative:

- A **distance** goal for rowing or elliptical. Suggest a time goal.
- A **send-off** (`distanceAndDuration`) goal for anything except swimming.
- A **distance** goal for any gym activity.

## 3. Choose the shape

- **`singleGoalWorkout`**: one steady effort with one time or distance goal
  ("30 min run", "5k", "1 hour ride").
- **`customWorkout`**: anything with intervals, a warmup, a cooldown, or
  varying intensity. `blocks` is an array of `{ steps, iterations }`. Each
  step has a `purpose` of `work` or `recovery`, a `goal`, and optionally an
  `alert` and a `displayName`. Blocks can't nest. Separate repeated sections
  (such as a kick set and then a pull set) are separate blocks.

Field rules that are easy to get wrong:

- Time goals are always **seconds** (`targetDuration: 1800`, `unit: "seconds"`).
- Distance units are full words: `kilometers`, `miles`, `meters`, `yards`.
- Use lowercase camelCase for `activityType`. Set `location` to `outdoor` by
  default, and to `indoor` for rowing, elliptical, gym activities, and pool
  swims.
- `swimmingLocation` is `""` for anything that isn't a swim, and `pool` (the
  default) or `openWater` for swims.
- Only use `warmup` for an explicitly requested or clearly preparatory
  segment. Don't move the main effort there just because it's easy.

### Intensity: heart-rate zone alerts

| Zone | User words |
|---|---|
| 1 | warmup, cooldown, recovery |
| 2 | easy, light, conversational, aerobic |
| 3 | moderate, tempo, steady, comfortably hard |
| 4 | hard, threshold |
| 5 | very hard, max, all-out, sprint, VO2 max |

### Swimming: send-off vs fixed rest

The two patterns look alike but use different shapes:

- **Send-off**, "4 x 100 @ 1:45" or "on the 1:45": one work step with a
  `distanceAndDuration` goal (`targetDistance`, `distanceUnit`, and
  `targetDuration` in seconds), with `iterations: 4`. **Don't** add a
  recovery step. The watch waits out the rest of the interval on its own.
- **Fixed rest**, "4 x 100 with 20s rest": a `distance` work step followed by
  a `time` recovery step.

For stroke and drill labels, use step `displayName`, and only these terms:
Freestyle, Backstroke, Breaststroke, Butterfly, IM, Kick drill, Pull drill,
Drill. If the user didn't name a stroke, leave `displayName` out.

### Gym and HIIT

WorkoutKit has no reps, sets, rounds, or load. Those details only ever go in
`displayName` text. Use `highIntensityIntervalTraining` for EMOM, AMRAP, and
circuits, `functionalStrengthTraining` for free weights and bodyweight,
`traditionalStrengthTraining` for machines, and `crossTraining` for mixed
workouts.

- **EMOM**: one 60 s time step, `displayName: "10 burpees"`, with
  `iterations` set to the number of minutes.
- **Circuit**: a time work step per exercise, each named, with time recovery
  steps, in one block where `iterations` is the round count.
- **AMRAP**: one time step (or a `singleGoalWorkout`) for the time cap, with
  the full round written out in `displayName`. Don't repeat it as rounds.
- **Straight sets** ("5x5 back squat @ 185lb"): `iterations: 5` over a 60 s
  placeholder time step with `displayName: "5 reps @ 185lb"`. Tell the user
  the timer is a placeholder.

## 4. Confirm, create, report

For anything beyond a single-goal workout, show the user a short outline
first (blocks, reps, goals, zones) and create it once they agree. Then call
`create_workout` with the workout object as the arguments. Don't wrap it in
another object.

Report the result based on `delivery`:

- `pushed`: delivery was requested and APNs accepted the push; Watch receipt is unconfirmed. If it is missing, inspect `get_workout_delivery_status` with the same `workout_id` and offer the returned `handoff_url` or QR. Missing or stale observations are unknown. Do not create a duplicate to retry delivery.
- `handoff`: give the user `handoff_url` to open on their iPhone.
- `not_delivered`: it was saved but the file couldn't be built. Say so
  plainly.

Mention the remaining `quota` when it is available. A `workout_saved` error still identifies an existing workout: inspect that ID rather than creating it again.

## Errors

- `invalid_workout`: read `issues`, fix the payload, and retry **once**. If it
  fails again, show the user the issues.
- `workout_limit_exceeded`: the weekly limit was reached. Stop.
- `subscription_required`: relay the returned entitlement message. Stop.
- `insufficient_scope`, or a 401 or auth error: ask the user to
  re-authenticate the `workouter` server: in Claude Code use `/mcp`; in OpenClaw use `openclaw mcp login workouter`. Approve the required permission; if it is not offered, remove and re-add the connector to refresh its requested scopes.
