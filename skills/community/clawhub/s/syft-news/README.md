# Clawhub Bundle: Syft CLI Skills

This directory is a Clawhub-compatible distribution bundle for the Syft CLI skill pack.

## Why This Bundle Exists

Some package hosts require a root-level `SKILL.md` in the top directory.
The original skill pack is modular and keeps most logic in subskill folders, so this bundle adds:

- a root-level `SKILL.md`
- a `subskills/` directory containing the orchestration skill plus five atomic skills

The root skill is intended to route the user request into the correct bundled subskill.

## Bundle Structure

- `SKILL.md`
- `README.md`
- `subskills/syft-news-pipeline/`
- `subskills/syft-profile-summary/`
- `subskills/syft-daily-briefing/`
- `subskills/syft-storyline-tree/`
- `subskills/syft-storyline-backfill/`
- `subskills/syft-guidance-rulebook/`

## Expected Behavior

Users enter through the root skill.
The root skill then tells the agent which bundled subskill to read based on the request:

- profile creation
- daily briefing
- storyline tree
- storyline backfill
- durable editorial guidance

## Runtime Assumptions

This bundle assumes the environment has access to:

- `syft following`
- `syft top`
- `syft search`

and can read files inside this package directory.

If the local environment does not have Syft CLI installed yet, install the official package first:

```bash
npm install -g @orionarm/syft-cli
```

Then complete login and verify the CLI:

```bash
syft login
syft status
```

After that, the root `SKILL.md` can route requests into the bundled subskills normally.
