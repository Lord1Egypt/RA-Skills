# Marketplace Packaging

Use one canonical skill folder as the source of truth. Do not maintain divergent copies for each marketplace.

## AgentSkills

Package the folder containing:

```text
SKILL.md
agents/openai.yaml
references/
scripts/
assets/
```

AgentSkills-style consumers should use the `SKILL.md` frontmatter to discover when to invoke the skill.

## Hermes / HermesHub

Hermes skills are reusable procedural memory. Publish the same folder and keep the default prompt focused on turning a competition idea into a replayable task repo. Do not add live secrets or validator credentials.

## Claw / OpenClaw

Treat Claw ecosystem distribution as untrusted by default. Publish only audited archives, pin versions, and include checksums for released packages. Do not install third-party skill packages into validator or production hosts without review.

## Release Checklist

- No secrets, mnemonics, private keys, API tokens, wallet files, or production env files.
- `SKILL.md` is concise and references detailed docs instead of embedding everything.
- Scripts compile and run from a clean checkout.
- Asset templates do not include live endpoints unless they are public.
- Archive hash is recorded after packaging.
- The marketplace description says the skill creates task repos; it does not run validators or handle funds.

