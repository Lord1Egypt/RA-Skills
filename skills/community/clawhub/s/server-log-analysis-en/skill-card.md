## Description:

Connect to remote servers over SSH, read sibling config.yaml to understand service metadata and log locations, download only required log snippets to local temp for analysis, and diagnose issues from evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to troubleshoot remote service issues by scoping incidents, checking configured log locations over SSH, downloading minimal log snippets, and reporting evidence-backed diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default configuration uses root SSH access and an inline password field.

Mitigation: Replace the sample connection with a least-privilege SSH account and use a secret manager, environment reference, or key-based authentication before installation.

Risk: Downloaded log snippets may contain sensitive operational or user data and are preserved by default.

Mitigation: Store snippets in a restricted per-session location and change retention so downloads are deleted by default unless preservation is explicitly required.

Risk: Remote log investigation can fetch more data than necessary if the scope is too broad.

Mitigation: Use the documented workflow to define a target service, host, time window, and candidate files, then prefer remote filtering or tail output before downloading logs.

## Reference(s):

- [Reference Notes](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/server-log-analysis-en)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnosis with evidence, confidence, suggested next steps, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local log snippet files under the configured temporary directory during investigations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
