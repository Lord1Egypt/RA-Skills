## Description:

Estimate how much of a git repository is AI-assisted and how sloppy it is. Use when the user asks whether a repo (or recent work) is "vibe coded", wants an AI-slop score, a repo health/quality snapshot, a badge, or a CI gate based on commit history. Read-only - commit metadata only, no file contents, no network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thiennhant95](https://clawhub.ai/user/thiennhant95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use vibegit to review commit-history signals, produce repository health reports and badges, and optionally set a CI score threshold. Its AI-assisted figure is an estimate of visible signals, not proof of authorship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a mismatch between the stated read-only, no-network purpose and documented install or clone commands; the supplied evidence does not verify downloaded-script behavior beyond its help command.

Mitigation: Review the documented setup commands and verify the script's behavior in the intended environment before use.

Risk: Heuristic scores can miss AI-assisted work and can be skewed by shallow or long-lived repository history; they do not establish authorship or correctness.

Mitigation: Treat scores as estimates, inspect the signal breakdown, use a suitable history window, and avoid treating the result as proof of authorship or code quality.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/thiennhant95/skills/vibegit)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, SVG badge]

**Output Format:** [Text overview, Markdown or JSON report, shareable one-line summary, or SVG badge]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A 0–100 score, estimated AI-assisted share with confidence band, and per-signal breakdown; output depends on the selected format.]

## Skill Version(s):

1.0.3 (source: release evidence, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
