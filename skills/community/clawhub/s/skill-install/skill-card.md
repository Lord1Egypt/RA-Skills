## Description:

Install Claude skills from GitHub repositories with automated security scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to browse, security-scan, select, and install Claude skills from GitHub repositories into a local Claude environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing remote third-party skills can permanently add instructions and scripts to the user's local Claude environment.

Mitigation: Use trusted repositories, prefer immutable commit URLs, review the file list and SKILL.md content, and confirm before installation.

Risk: The built-in scan is LLM-based and can be influenced by the remote skill content being scanned.

Mitigation: Treat SAFE results as a screening signal rather than a guarantee, and manually review warnings, unexpected tool use, and sensitive file or network behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/skill-install)
- [Security scan prompt](artifact/references/security_scan_prompt.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown text with security findings, installation decisions, and install summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide persistent installation of selected skill files after security review and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
