## Description:

Set up a reusable X/Twitter growth automation system with OpenClaw, Bird CLI, X API, optional source branching, optional community CTA, dry-run/live rollout, anti-repetition controls, and niche-specific posting policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roskva000](https://clawhub.ai/user/roskva000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install or adapt a reusable X/Twitter automation scaffold for a specific account, niche, language, cadence, and rollout mode. It guides setup questions, generates project files, and keeps live publishing gated behind explicit caps and approval choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can overwrite files in the target folder.

Mitigation: Run it in a new empty directory and review generated config before adding credentials.

Risk: Live X/Twitter publishing can post externally visible content if enabled.

Mitigation: Keep dry-run enabled first, then enable live publishing only after explicit caps, approval rules, reply policy, and source-branching behavior are configured.

Risk: Reply automation is higher risk than normal posting because targets may reject replies or create unwanted outreach.

Mitigation: Leave reply automation disabled by default, validate reply targets when possible, and record posted, skipped, and failed outcomes.

Risk: Repeated or same-source posts can occur when automation reuses similar drafts or mutable de-duplication keys.

Mitigation: Use stable slot keys, recent-post similarity checks, and source de-duplication before assigning live slots.

## Reference(s):

- [Setup Questionnaire](references/setup-questionnaire.md)
- [Rollout Modes](references/rollout-modes.md)
- [Operational Hardening](references/operational-hardening.md)
- [ClawHub Skill Page](https://clawhub.ai/roskva000/skills/x-growth-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scaffold output includes configuration JSON, Markdown operator notes, prompt files, an environment template, and helper scripts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
