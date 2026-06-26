# Install guide

This document describes the smallest practical installation flow for `personal-hooks` in an existing OpenClaw environment.

Release posture:

- V2 public mainline package
- publication gate defined by `docs/release-acceptance.md`
- optional host glue remains opt-in

## Positioning

`personal-hooks` is:

- an OpenClaw V2 continuity/follow-up skill package
- browser/local-gateway first
- usable without one specific chat platform for its core behavior

It is not:

- a standalone app
- a single-platform package
- a replacement for the host agent's own soul/persona

## Expected directory layout

Typical workspace layout:

```text
openclaw-workspace/
  skills/
    personal-hooks/
      SKILL.md
      scripts/
      docs/
      examples/
```

## Where to place the skill

Place the repository in your OpenClaw skills directory:

```text
/path/to/openclaw-workspace/skills/personal-hooks
```

You can either:

- copy the package into `skills/`
- symlink it into `skills/`
- install from a GitHub checkout
- install from a release ZIP
- install from an npm tarball produced by `npm pack`

Install the required Python dependency for the core skill:

```bash
python3 -m pip install -r requirements.txt
```

## Copy install

```bash
cp -R /path/to/personal-hooks /path/to/openclaw-workspace/skills/personal-hooks
```

## Symlink install

```bash
ln -s /path/to/personal-hooks /path/to/openclaw-workspace/skills/personal-hooks
```

## Helper scripts

The package includes one bundled install helper:

Portable skill-only helper:

```bash
bash scripts/install_local.sh /path/to/openclaw-workspace/skills link
```

Supported modes:

- `link`
- `copy`

The helper only installs the skill directory into a target skills folder and prints the next commands to run. It does not modify any channel configuration.

This public V2 package does not bundle a root-level `install.sh`.
If an operator wants a workspace-wide wrapper around the portable skill,
that wrapper should live outside the portable package.

## npm tarball packaging

The repository includes a minimal `package.json` so the exact same skill folder
can be packed as an npm tarball:

```bash
npm pack
```

That tarball is still installed as an OpenClaw skill folder. It does not turn
the skill into a Node-only runtime package.

## ClawHub-style packaging

The repository also includes `_meta.json` so the package can be indexed by
ClawHub-style skill catalogs without changing the runtime payload.

## Default vs host integration

Default installation installs the **skill package only**.

It does **not** automatically:

- install a host adapter plugin
- patch gateway runtime files
- change outbound channel behavior

If you need host-side outbound filtering or channel delivery behavior, implement
and test it in the host adapter for your own deployment. This package does not
ship an installable channel adapter.

If the host uses background heartbeat pushes, also configure heartbeat session
isolation in `openclaw.json`:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "heartbeat": {
          "every": "30m",
          "target": "direct-channel",
          "to": "[CHANNEL_DESTINATION]",
          "directPolicy": "allow",
          "lightContext": true,
          "isolatedSession": true
        }
      }
    ]
  }
}
```

Use `target: "direct-channel"` when you are routing to an explicit channel destination.
If you want the gateway to reuse the last external session instead, use
`target: "last"` and omit `to`.

`isolatedSession=true` keeps heartbeat background runs out of the main direct
conversation session, so the host can still push follow-ups without polluting
normal carryover/continuity state.

Before enabling it in production, verify the session/transcript behavior on the
exact OpenClaw version you are running. Heartbeat isolation is useful, but host
implementations and transcript handling can differ by version.

If the host adapter contributes runtime context, keep that integration aligned
with the shared skill version. Recent public-package fixes rely on host runtime
context preserving `time_modifier_prompt` and the post-`/new`
low-information continuity guard when those surfaces are available.

### Simple rule of thumb

Installing the skill alone gives you the shared follow-up/continuity engine.

If you also want full live channel behavior, the host may still need to wire:

- **Channel adapter / outbound last-defense**
- **gateway hook wiring**
- **live heartbeat host glue**

Those pieces are host/operator work. They are not auto-applied by the portable
skill package.

## Settings path

The public package expects writable runtime state outside the package itself.

Useful runtime environment variables:

- `PERSONAL_HOOKS_DATA_DIR`
- `PERSONAL_HOOKS_MEMORY_DIR`
- `PERSONAL_HOOKS_SESSIONS_INDEX_PATH`
- `PERSONAL_HOOKS_JOBS_PATH`
- `PERSONAL_HOOKS_OPENCLAW_CONFIG_PATH`
- `PERSONAL_HOOKS_SETTINGS_PATH`

Start from:

- `examples/settings.sample.json`
- `config.schema.json`
- `docs/host-operator-settings.md`

The most common settings are:

- `followup.enabled`
- `sleep_rest_suppress.enabled`
- `sleep_rest_suppress.duration_hours`
- `carryover.enabled`
- `carryover.max_turns`
- `dispatch.cooldown_minutes`
- `dispatch.cap`
- `closure.auto_close_on_user_reply`

For deterministic first-run and guided-settings behavior, the current public
package now expects the shared skill to own these fields directly:

- onboarding:
  - `timezone`
  - `sleep_time`
  - `wake_time`
  - `relationship`
  - `use_case`
  - `new_session_continuity_mode`
  - `modality_continuity_mode`
- guided settings:
  - `proactive_chat.enabled`
  - `proactive_chat.interval_hours`
  - `proactive_chat.quiet_hours`
  - `re_engagement.mode`
  - `re_engagement.retry_after_hours`
  - `re_engagement.max_unanswered_before_park`
  - `routine_schedule.phases.active_day.interval_hours`
  - `new_session_continuity.mode`
  - `modality_continuity.mode`

`experimental.rhythm_nudge.enabled` is intentionally `false` by default and is not required for the public package.

For operator-facing knobs such as tracking lifetime, carryover depth,
routine schedule, and quiet-hours policy, see:

- `docs/host-operator-settings.md`

## Initialization

After installation:

```bash
python3 /path/to/openclaw-workspace/skills/personal-hooks/scripts/personal_hooks.py init
```

## Minimal state check

```bash
python3 /path/to/openclaw-workspace/skills/personal-hooks/scripts/personal_hooks.py capability-state-show
```

## Minimal verification

```bash
python3 /path/to/openclaw-workspace/skills/personal-hooks/scripts/followup_skill_harness.py --absence-minutes 3
```

The regression harness and the optional `web_live_runner.mjs` are included in
the public release package for reproducible local verification. They are test
helpers, not runtime requirements.

## Browser/local-gateway-first usage

The intended public V2 path is:

- install the skill into an OpenClaw workspace
- initialize it
- use it through the ordinary reply pipeline
- validate with browser/local gateway if desired

Channel-specific delivery is optional for package validation and is not required for the core skill behavior.

If you want channel-facing frontstage stopgap behavior, implement it in the host
adapter for your channel. The skill package itself stays portable and
channel-neutral.

## Common troubleshooting

If the skill does not initialize:

- verify the package is under the correct `skills/` directory
- verify Python 3 is available
- verify the runtime state path is writable

If capability state looks empty:

- run `init` first
- verify `PERSONAL_HOOKS_DATA_DIR` is pointing where you expect

If the harness cannot build a sandbox:

- verify your temp directory is writable
- verify optional OpenClaw config paths only if you need embedding fallback

If browser/local gateway usage does not reflect continuity state:

- verify the host OpenClaw environment is actually loading the skill from the intended `skills/` directory
- verify the ordinary reply pipeline uses the installed package, not another local copy
