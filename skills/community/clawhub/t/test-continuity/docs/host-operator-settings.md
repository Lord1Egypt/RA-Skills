# Host Operator Settings

This document is for host operators who want to tune:

- how long tracked state should live
- how routine schedule should be applied
- how quiet / rest / work-time behavior should be applied
- which knobs belong to the portable skill, and which still belong to host/live

The public package stays skill-first. Host-specific delivery or persona choices
should still live outside the portable core.

## 0. Causal memory boundary: what the public skill should and should not do

The public package should:

- extract causal structure from recent conversation
- preserve continuity facts, user state, unresolved loops, and time anchors
- write structured continuity state into staging / tracked follow-up / daily-memory paths
- give the model enough internal context to continue naturally later

The public package should **not**:

- hardcode role-specific push wording
- prewrite what one specific host should say
- assume one host role, one language, or one chat platform

In other words:

- the skill owns structured continuity state
- the model owns natural language generation
- the host owns delivery, persona, and platform specifics

## 0.5. Host-agnostic settings entry

The public package should expose one simple natural-language entry into guided
settings mode, without binding the skill to one specific chat platform or any other single
external platform.

Recommended multilingual entry phrases:

- Traditional Chinese: `幫我調整關心設定`
- Simplified Chinese: `帮我调整关心设置`
- English: `Help me adjust my follow-up settings`
- Japanese: `フォローアップ設定を調整して`
- German: `Hilf mir, meine Follow-up-Einstellungen anzupassen`
- Italian: `Aiutami a regolare le impostazioni di follow-up`
- Spanish: `Ayúdame a ajustar mi configuración de seguimiento`

This entry should open a guided update flow, not directly mutate everything at
once. A host should:

1. run `setup-check`
2. identify which category the user wants to change
3. apply only changed fields through `setup-apply`

Recommended guided categories:

- `schedule`
- `proactive`
- `tracking`
- `tone`

Important boundary:

- host/user can adjust policy values
- host/user should **not** directly tune causal extraction logic, continuity
  core rules, or daily-memory promotion internals

## 1. Tracking lifetime: what expires, and where to change it

There is no single "memory TTL" knob. Different layers have different lifetimes.

### Causal memory summary behavior

This is the public, host-agnostic operator surface for how much structured
continuity state is preserved in internal summaries. It affects the skill's
internal continuity context, not frontstage wording.

Public settings (in `causal_memory`):

- `summary_max_facts`: default `3`
- `include_time_anchor`: default `true`
- `include_state_marker`: default `true`

These control:

- how many factual clauses are retained in normalized continuity summaries
- whether time anchors such as `today`, `tonight`, `21:00`, or `Monday` stay visible
- whether neutral state markers such as `busy`, `tired`, or `sick` remain available to the model

This is useful for multilingual hosts because it keeps structure explicit
without forcing one frontstage phrasing style.

### Candidate staging TTL

Candidate staging is the short-term holding area before a topic is promoted into
formal incident/event tracking.

Public settings (in `candidate_ttl_hours`):

- `emotion`: 24 hours
- `support`: 24 hours
- `task`: 168 hours (7 days)
- `preference`: 168 hours (7 days)

Configurable via `settings.json` → `candidate_ttl_hours.*`.

### Carryover lifetime

Carryover controls how much of the last session can be pulled into a new
session.

Public setting:

- `carryover.max_turns`

Default sample value:

- `5`

Where to change it:

- host runtime settings file
- start from `examples/settings.sample.json`

Relevant files:

- `examples/settings.sample.json`
- `config.schema.json`

### Dispatch cooldown / follow-up lifetime

These determine how often follow-up **may** dispatch. The interval is a minimum re-evaluation window, not a guaranteed send frequency. Actual dispatch also depends on: whether the user has re-engaged, followup_state guards, cooldown, dispatch cap, quiet hours, and sleep/rest suppress.

Public settings:

- `dispatch.cooldown_minutes`
- `dispatch.cap`
- `proactive_chat.interval_hours`
- `proactive_chat.cooldown_minutes`
- `proactive_chat.max_proactive_per_day`

Default sample values:

- `dispatch.cooldown_minutes = 180`
- `dispatch.cap = 3`
- `proactive_chat.interval_hours = 3`
- `proactive_chat.cooldown_minutes = 180`
- `proactive_chat.max_proactive_per_day = 2`

### Re-engagement policy

Controls what happens after a dispatch receives no user reply.

Public settings (in `re_engagement`):

- `mode`: `"wait_for_reply"` (default) — park after `max_unanswered_before_park` dispatches; only user reply unparks. `"timed_retry"` — automatically retry parked hooks after `retry_after_hours` even without reply.
- `retry_after_hours`: `4` (default) — hours to wait before retrying a parked hook (only used when `mode=timed_retry`)
- `max_unanswered_before_park`: `2` (default) — how many dispatches without reply before the hook is parked

### Parked hook auto-close

Public setting (in `followup`):

- `followup.parked_auto_close_hours`: `0` (default, disabled) — if > 0, parked hooks are auto-cancelled after this many hours since last dispatch

### Temporal guard

Controls how recently a user must have interacted for dispatch guards to allow/block.

Public setting (in `temporal_guard`):

- `temporal_guard.newer_interaction_minutes`: `5` (default) — if user interacted this many minutes after the proactive anchor, block dispatch as "newer-user-interaction"

### Rest-suppress lifetime

When the user says they want to sleep or rest, the skill can suppress follow-up
for a fixed duration.

Public settings:

- `sleep_rest_suppress.duration_hours`: `10` (default) — how long rest-suppress lasts
- `sleep_rest_suppress.auto_clear_hours`: `4` (default) — auto-clear rest-suppress after this many hours even without explicit resume. Set to `0` to disable auto-clear.

### Same-type cooldown

There is also an internal same-type cooldown used by the skill to avoid
repeating the same kind of incident too often.

Current internal default:

- `same_type_cooldown_hours = 6`

This is currently a code-level default, not a public schema field.

## 2. Routine schedule: how to make the host apply sleep/wake timing

Use `routine_schedule` when the host knows the user's rough daily pattern and
wants proactive timing to come from a stable schedule instead of memory guesswork.

Main fields:

- `routine_schedule.enabled`
- `routine_schedule.timezone`
- `routine_schedule.sleep_time`
- `routine_schedule.wake_time`
- `routine_schedule.wake_window_minutes`
- `routine_schedule.phases.sleep.proactive_enabled`
- `routine_schedule.phases.sleep.wake_seed_enabled`
- `routine_schedule.phases.wake_window.proactive_enabled`
- `routine_schedule.phases.wake_window.wake_seed_enabled`
- `routine_schedule.phases.wake_window.interval_hours`
- `routine_schedule.phases.active_day.proactive_enabled`
- `routine_schedule.phases.active_day.wake_seed_enabled`
- `routine_schedule.phases.active_day.interval_hours`

Typical use:

- set `enabled=true`
- set `timezone`
- set one sleep time and one wake time
- decide whether wake-window should allow proactive and wake-seed
- decide active-day interval separately from wake-window

See also:

- `docs/routine-schedule.md`

## 3. Quiet mode: how to suppress proactive messages at fixed times

Use `proactive_chat.quiet_hours` when the host wants a stable blocked window.

Public fields:

- `proactive_chat.quiet_hours.start`
- `proactive_chat.quiet_hours.end`

Behavior:

- if `start == end`, quiet-hours is effectively disabled
- if `start < end`, the blocked window is same-day
- if `start > end`, the blocked window crosses midnight

Examples:

- `23 -> 7` means quiet overnight
- `9 -> 18` means quiet during workday
- `99 -> 99` is not a portable public convention; prefer disabling or using the
  same start/end value instead

## 4. Work-time behavior: what is public, what is still host/live

There are two different ways to model "working hours":

### A. Stable work hours

Use:

- `proactive_chat.quiet_hours`

This is the portable public way if the user usually does not want proactive
messages during fixed work hours.

### B. Dynamic "I am currently working" state

This is a host/live concern.

The live system may maintain a dynamic work-DND state when the user explicitly
says they are working, focused, or busy. That is not yet a portable public
schema block in RC.

For public packaging, the honest rule is:

- fixed work windows -> use `quiet_hours`
- dynamic current work state -> host/live extension

## 5. Rest / sleep phrases

The public skill already supports rest/sleep suppression logic.

Host operators should know:

- this is not the same as quiet-hours
- quiet-hours is a clock-based block
- rest-suppress is a user-state block

Recommended split:

- use `quiet_hours` for stable clock windows
- use `sleep_rest_suppress` for explicit "I want to sleep/rest now"

## 6. Minimum host workflow

For a portable install, the simplest order is:

1. copy or symlink the skill package into `skills/personal-hooks/`
2. create a writable runtime settings file from `examples/settings.sample.json`
3. tune:
   - `carryover.max_turns`
   - `new_session_continuity.mode`
   - `modality_continuity.mode`
   - `dispatch.cooldown_minutes`
   - `proactive_chat.*`
   - `routine_schedule.*`
   - `sleep_rest_suppress.duration_hours`
4. initialize the skill
5. verify continuity and follow-up in the host's ordinary reply pipeline

If the host also uses heartbeat-driven proactive pushes, add one more host-side
rule:

- set `heartbeat.isolatedSession=true`

Why this matters:

- heartbeat can legitimately deliver to the same user/channel
- but it should not reuse the same session key for background generation
- otherwise heartbeat prompts and dispatch context can leak back into ordinary
  continuity / carryover / staging state

Recommended host heartbeat shape:

```json
{
  "heartbeat": {
    "every": "30m",
    "target": "direct-channel",
    "to": "[CHANNEL_DESTINATION]",
    "directPolicy": "allow",
    "lightContext": true,
    "isolatedSession": true
  }
}
```

Before enabling it in production, verify the session/transcript behavior on the
exact OpenClaw version you are running. Heartbeat isolation is useful, but host
implementations and transcript handling can differ by version.

## 7. What is still not fully portable

The following should still be treated as host/live integration work:

- dynamic work-DND state
- channel-specific outbound delivery rules
- final outbound cleanup such as `<final>` / heartbeat leakage interception
