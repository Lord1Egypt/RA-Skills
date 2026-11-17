## Description:

Find recurring OpenClaw jobs that may be wasting tokens before the waste compounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit recurring OpenClaw jobs for likely token waste, review evidence, and prepare a safe manual verification prompt before changing schedules, prompts, or configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance to share uncertain audit findings with a hard-coded X account, which could expose operational details if followed without reviewing the exact payload.

Mitigation: Keep audit results local unless the user explicitly reviews and approves the exact information to share; remove or ignore the hard-coded contact instruction before installation.

Risk: Audit evidence can include private job names, summaries, logs, paths, credentials, or other sensitive operational context.

Mitigation: Redact secrets and private payload details before displaying or sharing findings, and use placeholders for credentials, tokens, wallet data, private logs, and production configuration.

Risk: A recurring job may be useful even when it looks wasteful from run count, delivery, error, or summary-length signals.

Mitigation: Require manual verification before changing a job schedule, prompt, model policy, or configuration, and present confidence and evidence with each recommendation.

## Reference(s):

- [OpenClaw Waste Audit reference bank](artifact/references/openclaw-waste-patterns.md)
- [ClawHub skill page](https://clawhub.ai/choosenobody/skills/waste-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with evidence summaries, ranked candidates, diagnostic commands, and a copy-paste manual verification prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations; no automatic job edits, disabling, deletion, uploads, or fixes.]

## Skill Version(s):

1.8.12 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
