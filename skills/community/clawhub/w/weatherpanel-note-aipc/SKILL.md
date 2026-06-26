---
name: weatherpanel-note-aipc
description: >
  WeatherPanel Note AI PC for Shanghai weather. This skill fetches current weather
  from Open-Meteo, summarizes the overall conditions with a local LLM through the
  summarize CLI, updates a local Canvas dashboard, and safely appends the summary
  to a Markdown note inside a configured Obsidian vault.
user-invocable: true
metadata:
  openclaw:
    emoji: "🌤️"
    homepage: https://open-meteo.com/en/docs
---

# WeatherPanel Note AI PC

## What this skill does

- Fetches current and hourly Shanghai weather from Open-Meteo.
- Generates a local summary with the installed `summarize` CLI.
- Updates the Canvas dashboard data for `weatherpanel-note-aipc`.
- Appends summary records to a Markdown note inside the configured Obsidian vault.

## Safety and ClawHub alignment

- Do **not** modify `HEARTBEAT.md`.
- Do **not** change global OpenClaw config.
- Do **not** create or run `.bat`, `.cmd`, or `.ps1` files.
- Do **not** use Windows Task Scheduler, startup folders, registry persistence, or shell profile persistence.
- Do **not** read generic secret-bearing files such as `env.bat`.
- Only run the Python scripts bundled with this skill.
- The weather source is fixed to Shanghai coordinates in bundled code.
- The summary step uses a shell-free subprocess call to the fixed command name `summarize` found on PATH.
- The Obsidian step does **not** invoke `obsidian-cli`; it writes only to a validated `.md` path under a configured vault directory inside the user's home directory.

## Default action

For a normal invocation, run the bundled pipeline:

```
python run_weatherpanel.py --mode all
```

Then tell the user the dashboard is available at the local Canvas path for this skill:

```
/__openclaw__/canvas/weatherpanel-note-aipc/dashboard.html
```

## Other requests

- Refresh weather now:
  ```
  python run_weatherpanel.py --mode all
  ```

- Fetch only:
  ```
  python run_weatherpanel.py --mode fetch
  ```

- Summarize only:
  ```
  python run_weatherpanel.py --mode summarize
  ```

- Flush queued summaries to the Obsidian-compatible Markdown note only:
  ```
  python run_weatherpanel.py --mode flush
  ```

- Prepare or refresh just the dashboard asset:
  ```
  python run_weatherpanel.py --mode prepare-dashboard
  ```

- Check token cost:
  read the file `token_cost.json` from the Canvas directory for `weatherpanel-note-aipc`.

## Optional configuration

This skill does not require secrets. If needed, it may read a dedicated allowlisted JSON config file at:

```
~/.openclaw/state/weatherpanel_note_aipc/config.json
```

Supported keys are limited to:

- `CANVAS_ROOT`
- `OBSIDIAN_VAULT`
- `OBSIDIAN_NOTE_PATH`
- `OPENCLAW_BASE_URL`
