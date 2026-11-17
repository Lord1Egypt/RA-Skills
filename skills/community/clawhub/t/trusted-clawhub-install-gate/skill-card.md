## Description:

Audit a local OpenClaw or ClawHub skill directory before installation, classify it as PASS, REVIEW, or BLOCK, check active-project impact, and optionally run the clawhub-install-gate CLI to write a receipt or install after explicit user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect local OpenClaw or ClawHub skill artifacts before installation, understand PASS, REVIEW, or BLOCK findings, and decide whether staging or installation is appropriate. It is intended to make install decisions explicit, especially when replacement, REVIEW override, global installation, or project-impact risks are present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing, replacing, or globally enabling a skill can affect the active project or future agent behavior.

Mitigation: Run the inspection first, review the active-project impact report, and require explicit user approval for REVIEW overrides, replacements, or global installs.

Risk: The required clawhub-install-gate CLI may come from an untrusted or unexpected source.

Mitigation: Confirm the CLI source before installation and review the inspection findings before allowing the skill to run install commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/trusted-clawhub-install-gate)
- [Publisher profile](https://clawhub.ai/user/zack-dev-cm)
- [Project homepage](https://github.com/zack-dev-cm/trusted-clawhub-install-gate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS, REVIEW, or BLOCK classification, active-project impact notes, and approval requirements before installation.]

## Skill Version(s):

0.2.2 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
