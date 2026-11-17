# Transfer Consciousness

Preserve context and coordinate single-owner handoffs across hosts.

## Why it is useful

A fresh session loses the reasons behind earlier decisions; a careless handoff can also leave two agents making changes. Transfer Consciousness preserves the continuation brief and separates destination readiness from permission to take over.

## Install

```bash
npx skills add AntreasAntoniou/transfer-consciousness
```

Or place this repository in your agent's skill directory and load [SKILL.md](SKILL.md).

## Try it

“Prepare a handoff of this project to my chosen server. Verify the files and destination readiness, but do not give the destination write ownership until the source is quiesced.”

## What is included—and what is not

This is an instruction skill, not a daemon, scheduler, remote runtime or enforcement service. It requires a reachable user-approved destination and existing runtime. Single-writer enforcement requires a real lock/lease or a disclosed supervised cutover; the prompt itself is not a distributed lock. No private transcripts, machine inventory or credentials are included.

## Validation

The public instructions are independently scenario-reviewed for scope, authority and failure behaviour. That is not proof that every model follows them. Test in your own environment before consequential use.

MIT licensed. By [Antreas Antoniou](https://antreas.io/skills/).
