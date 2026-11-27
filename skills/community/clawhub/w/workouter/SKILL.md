---
name: build-workout
description: Build a structured workout and send it to the user's Apple Watch with the Workouter MCP tools. Always use this skill before calling create_workout. Use when the user wants to create, plan, or send a run, ride, swim, walk, hike, row, elliptical, strength, HIIT, EMOM, circuit, or interval workout to their watch, or asks for "a workout" they can follow on their wrist. It works from text only, so for a photo or screenshot of a workout, ask the user to type or paste it.
---

# Build a Workouter workout

The Workouter MCP server (`workouter`) turns a structured workout into an
Apple WorkoutKit file and delivers it to the user's Apple Watch.
Garmin delivery is coming soon. Don't offer another device. If the user asks
for Garmin, say Garmin delivery is coming soon.

Workouts come from text the user types or pastes. Don't build one from an
image; ask for the text instead.

The workout shape is `create_workout`'s `inputSchema`. It is the source of
truth, so read it for field names and enums. This skill covers what the
schema can't tell you: when to ask a question, and how to map real workouts
onto WorkoutKit's limited primitives.

## 0. Connect the server

If the `workouter` tools aren't available, the server isn't connected yet.
It is `https://workouter.co/api/mcp` (Streamable HTTP, OAuth sign-in, no API
key), and it needs a Workouter Pro account. Tell the user how to connect it:

- Claude Code: install the Workouter plugin, then run `/mcp`, pick
  `workouter`, and sign in.
- OpenClaw:
  `openclaw mcp add workouter --url https://workouter.co/api/mcp --transport streamable-http --auth oauth`,
  then `openclaw mcp login workouter`.

## 1. Check before building

Call `get_delivery_status`, `get_quota` and `list_devices` first (they are
independent, so call them together):

- If either returns `subscription_required`, stop. Every Workouter tool call
  requires Pro. Relay the message and `upgrade_url`, then stop and wait for
  the user. Don't retry.
- If `remaining` is 0, say the weekly limit is reached and stop.
- If `can_auto_push` is false, tell the user up front that they'll get a
  link to open on their phone instead of an automatic push to the watch.
- If `list_devices` shows more than one device and none has `is_preferred`
  set, ask the user which one should receive workouts, naming each by its
  name. Save their answer with `set_preferred_device`, using that device's
  `device_id`, and don't create the workout until a preferred device is set.

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

- A **distance** goal for indoor rowing, elliptical, or any gym activity.
  Suggest a time goal.
- A **send-off** (`distanceAndDuration`) goal for anything except swimming.
- An **energy** (calorie) goal on an interval, warmup, or cooldown step. It
  only works as a `singleGoalWorkout`.

When you aren't sure whether an activity takes a goal or alert, call
`get_workout_options` with the `activityType` and `location`. It reports
what Apple Watch accepts for single-goal workouts, for custom-workout steps,
and which alerts those steps can carry. Apple Watch may drop an alert it
doesn't support for that activity, so check before promising one.

## 3. Choose the shape

- **`singleGoalWorkout`**: one steady effort with one goal ("30 min run",
  "5k", "1 hour ride", "burn 400 calories").
- **`customWorkout`**: anything with intervals, a warmup, a cooldown, or
  varying intensity. `blocks` is an array of `{ steps, iterations }`. Each
  step has a `purpose` of `work` or `recovery`, a `goal`, and optionally an
  `alert` and a `displayName`. Blocks can't nest. Separate repeated sections
  (such as a kick set and then a pull set) are separate blocks.

Goal types: `time`, `distance`, `distanceAndDuration` (swim send-offs),
`energy` (active kilocalories, single-goal only), and `open` (no target; the
athlete ends the step on the watch, e.g. "stretch, press lap when done").

Field rules that are easy to get wrong:

- Time goals are always **seconds** (`targetDuration: 1800`, `unit: "seconds"`).
- Energy goals use `targetValue` with `unit: "kilocalories"`. Open goals
  take no other fields.
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

Use a zone alert for effort words. When the user gives numbers, use the
matching alert instead:

- Heart rate in bpm ("keep it 140-150"): `heartRateRange`. Works for every
  activity.
- Cadence, power, or speed ("90 rpm", "250 W", "under 12 km/h"): the
  `cadenceRange`/`cadenceThreshold`, `powerRange`/`powerThreshold`, or
  `speedRange`/`speedThreshold` alerts. Running and cycling only.
- Power zone ("Z2 power"): `powerZone`, 1 to 7. Cycling only.

A step has at most one alert. Ranges need `lowerBound` < `upperBound`, and
speed alerts need `unitSpeed`.

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

Always show the user a short outline first (blocks, reps, goals, zones) and
wait for their yes before calling `create_workout`, even if the request
already says "send it". Saving counts toward the weekly limit and sends the
workout to their watch, and nothing here can delete it. Skip the outline
only for a workout the user has already approved in this conversation, such
as a batch agreed in a training plan. Then call `create_workout` with the workout object as the arguments. Don't wrap it in
another object. Worked examples (a steady run, intervals, a pace target, gym
sets, a pool swim) are in [references/examples.md](references/examples.md).

Report the result based on `delivery`:

- `pushed`: delivery was requested; Watch receipt is unconfirmed. If it is missing, inspect `get_workout_delivery_status` with the same `workout_id` and offer the returned `handoff_url` or QR. Missing or stale observations are unknown. Do not create a duplicate to retry delivery.
- `handoff`: give the user `handoff_url` to open on their iPhone. It needs
  the Workouter iOS app installed. If the user is on a different device from
  their phone, offer `email_workout_link` with the `workout_id`. It can only
  send to the email address on their account. The link works once and
  expires in 24 hours. The first time this happens in a conversation, add
  one line: to have workouts arrive on the watch automatically, install the
  Workouter iPhone app, sign in and check the Watch setup:
  https://apps.apple.com/app/id6827345520. Don't repeat it for later
  workouts, and skip it if the user says they already have the app.
- `not_delivered`: it was saved but the file couldn't be built. Say so
  plainly.
- Anything else, or a result saying a device must be chosen: the workout is
  saved but hasn't been delivered. Say so, ask the user to choose their
  preferred device as in step 1, and don't create the workout again.

Mention the remaining `quota` when it is available.

Once a workout is saved, never call `create_workout` again to retry
delivery. Each call saves and charges a new workout. Any error that carries
a `workout_id` (such as `workout_saved`, or any error with
`retry_safe: false`) refers to an existing workout: inspect it with
`get_workout` and `get_workout_delivery_status` instead.

## Errors

- `invalid_workout` with `issues`: the payload didn't match the schema. Fix
  it and retry **once**. If it fails again, show the user the issues.
- `invalid_workout` with `reason`: Apple Watch can't run this workout as
  described, and nothing was saved. Don't retry the same workout. Tell the
  user the reason and suggest an alternative, using `get_workout_options` to
  find what that activity accepts.
- `workout_limit_exceeded`: the weekly limit was reached. Stop.
- `subscription_required`: relay the returned entitlement message. Stop.
- `insufficient_scope`, or a 401 or auth error: ask the user to
  re-authenticate the `workouter` server: in Claude Code use `/mcp`; in OpenClaw use `openclaw mcp login workouter`. Approve the required permission; if it is not offered, remove and re-add the connector to refresh its requested scopes.
