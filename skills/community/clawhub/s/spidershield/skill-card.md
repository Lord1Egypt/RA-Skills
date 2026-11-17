## Description:

SpiderShield Security Scanner provides OpenClaw skill trust lookups, malware scanning, configuration auditing, auto-fix guidance, tamper pinning, and bulk installed-skill scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teehooai](https://clawhub.ai/user/teehooai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to assess OpenClaw skills and installations through trust-score lookup, local malware scans, configuration audits, auto-fix review, and content-hash pinning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local commands delegate scanning and configuration-changing work to an external Python package that is not pinned by the skill artifact.

Mitigation: Use a pinned and trusted spidershield package or an isolated virtual environment before running local scan, audit, fix, pin, or scan-all commands.

Risk: Configuration fixes can modify files under ~/.openclaw.

Mitigation: Run /spidershield fix --dry-run first and review the proposed ~/.openclaw changes before confirming fixes.

Risk: The security review reports an unsafe Python import fallback in the local command wrappers.

Mitigation: Run local commands only from a trusted directory and prefer a trusted installed spidershield CLI over import fallback execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teehooai/skills/spidershield)
- [SpiderRating Trust Registry](https://spiderrating.com)
- [Publisher profile](https://clawhub.ai/user/teehooai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style command guidance and terminal text output, including trust reports, scan findings, audit results, and configuration-change previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The check command calls the SpiderRating API with an author/skill slug; local scan, audit, fix, pin, and scan-all commands depend on the spidershield Python package.]

## Skill Version(s):

0.3.0 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
