## Description:

Creates and manages automated trading strategies and protective trade rules for Polymarket and HyperLiquid through the Vincent CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, monitor, pause, archive, and inspect automated trading strategies and position protection rules. It helps agents prepare Vincent CLI commands and configuration for strategy drivers, thesis rules, trade limits, event review, and cost monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for automated trading with wallet-linked authority.

Mitigation: Use revocable, least-privilege trading keys, strict server-side trade limits, and explicit approval thresholds.

Risk: The skill runs a mutable third-party CLI through npx.

Mitigation: Prefer a pinned, vetted @vincentai/cli version or a preinstalled binary before use.

Risk: Broad filesystem access could expose files beyond the required wallet reference and working directory.

Mitigation: Run it in a confined environment and grant only the filesystem access needed for the wallet reference and active workspace.

## Reference(s):

- [Vincent Homepage](https://heyvincent.ai)
- [ClawHub Skill Page](https://clawhub.ai/glitch003/skills/vincent-trading-engine)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline bash and JSON blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy configuration, rule parameters, command examples, and status or log interpretation.]

## Skill Version(s):

1.0.69 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
