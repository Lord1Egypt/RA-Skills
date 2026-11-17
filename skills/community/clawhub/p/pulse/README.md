# Pulse

Recurring agent checks that know what to inspect, when to speak and when to stop.

## Why it is useful

A vague recurring prompt becomes noise—or keeps running after its purpose has disappeared. Pulse gives every watch an exact target, evidence source, notification rule, authority boundary and stopping condition. Meta-Pulse reviews the whole set for gaps, duplicates and stale assumptions.

## Install

```bash
npx skills add AntreasAntoniou/pulse
```

Or place this repository in your agent's skill directory and load [SKILL.md](SKILL.md).

## Try it

“Watch this deployment until it finishes. Tell me on completion, failure or anything needing my input. Keep quiet otherwise, and stop the watch when it is done.”

## What is included—and what is not

This is an instruction skill, not a daemon, scheduler, remote runtime or enforcement service. It requires a supported scheduler in the host agent; this repository does not schedule anything by itself. No private transcripts, machine inventory or credentials are included.

## Validation

The public instructions are independently scenario-reviewed for scope, authority and failure behaviour. That is not proof that every model follows them. Test in your own environment before consequential use.

MIT licensed. By [Antreas Antoniou](https://antreas.io/skills/).
