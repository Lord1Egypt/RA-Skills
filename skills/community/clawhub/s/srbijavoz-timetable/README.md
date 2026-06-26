# Srbija Voz Train Status Skill

<img width="640" alt="Srbijavoz skill cover" src="https://github.com/user-attachments/assets/86769c9c-2d6b-4349-a3ab-11a647dc7189" />

Use this skill when you want an agent to check current Srbija Voz notices, look up stations, and quickly tell you whether a train issue is a delay, cancellation, stoppage, operational change, or replacement bus service.

## What it does

The skill is built to:

- pull current notices from the official API
- resolve station names from partial input
- classify notice text into a user-friendly disruption type

## How to use it

Once the skill is installed, ask in plain language.

Example prompts:

- "Check Srbija Voz for delays between Petrovaradin and Beograd centar"
- "Look up the station name for Bataj"
- "Is there a current cancellation notice for Novi Sad trains?"
- "Check whether the Petrovaradin to Novi Sad bus notice is just regular service info"

## Install in Codex

```bash
cp -R /path/to/srbijavoz ~/.codex/skills/
```

After that, the skill can be invoked as `srbijavoz`.

## Install in OpenClaw

Copy the skill folder into your OpenClaw skills directory:

```bash
cp -R /path/to/srbijavoz ~/.openclaw/skills/
```

If your OpenClaw setup uses a workspace-based skills folder instead, copy it into that environment's `skills/` directory so OpenClaw can discover the folder as `srbijavoz`.

## Install in Claude Code

```bash
cp -R /path/to/srbijavoz ~/.claude/skills/
```

If your setup uses a different skills directory, copy the folder there instead.

## What to expect in answers

Good answers should be short, clear, and useful to a passenger first.

They should usually include:

- whether there is a current issue or not
- the affected route, train, or departure times if known
- whether it looks like a fresh same-day issue, an ongoing arrangement, or a recurring timetable notice
- what the passenger should do next, if obvious

They should usually avoid internal classifier jargon unless the user explicitly asks for it.

## Example of a good user-facing summary

```text
Today on the Novi Sad to Belgrade railway, there was a morning disruption, but not a full-day line shutdown.

What I found:
- A Petrovaradin ↔ Beograd centar service was disrupted this morning
- The 07:20 from Petrovaradin to Beograd centar and the 08:30 return did not run on the Batajnica ↔ Beograd centar segment
- I did not find a broader fresh notice saying the whole Novi Sad ↔ Belgrade corridor is down all day

What this means in practice:
- There was a real issue this morning on the corridor
- The line does not appear to be generally suspended for the rest of today, based on the notices I saw
```

Why this is good:

- leads with the practical verdict
- keeps only route and time details that matter
- separates facts from interpretation
- avoids internal classification language unless the user asks for it

## Run the bundled script directly

If you want to use the scraper outside the agent flow:

```bash
python3 scripts/srbvoz_scraper.py --query "kašnjenje" --limit 20
python3 scripts/srbvoz_scraper.py --station "Beograd"
python3 scripts/srbvoz_scraper.py --timetable-info
```

Useful options:

- `--query` filters notices by substring
- `--limit` limits how many notices are returned
- `--station` resolves station autocomplete matches
- `--timetable-info` fetches timetable page metadata
- `--no-fallback` disables HTML fallback behavior
