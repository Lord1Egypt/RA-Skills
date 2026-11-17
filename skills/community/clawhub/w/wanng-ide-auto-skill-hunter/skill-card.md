## Description:

Proactively discovers, ranks, and installs high-value ClawHub skills by mining unresolved user needs and agent context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover, rank, preview, and optionally install ClawHub skills for unresolved tasks or capability gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mine recent conversations and workspace memory, which may expose private tasks or sensitive context.

Mitigation: Run dry-run mode first and avoid use in workspaces containing private conversations, credentials, or sensitive data unless access boundaries are reviewed.

Risk: Live install mode can install third-party skills and run downloaded or generated code.

Mitigation: Review and scan selected skills before live install, keep max-install low, and use an isolated workspace for evaluation.

Risk: The skill can send recommendation reports to an external reporting path.

Mitigation: Set SKILL_HUNTER_NO_REPORT=1 during local tests or whenever outbound reporting has not been explicitly approved.

## Reference(s):

- [Wanng Ide Auto Skill Hunter - ClawHub](https://clawhub.ai/terrycarter1985/skills/wanng-ide-auto-skill-hunter)
- [Memory Mesh Core - ClawHub](https://clawhub.ai/wanng-ide/memory-mesh-core)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style recommendation report with command-line status text and generated skill files when live install is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live install mode may clone or scaffold up to the configured max-install count; dry-run mode previews selections without installing.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
