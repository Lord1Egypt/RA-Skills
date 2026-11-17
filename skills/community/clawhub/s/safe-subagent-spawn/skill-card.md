## Description:

Safely create and manage subagents through a strict wrapper instead of calling sessions_spawn directly, with multi-round continuity via shared context files with full-text history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devymex](https://clawhub.ai/user/devymex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate work to subagents through validated helper scripts, preserve full-text context across rounds, and reduce mistakes in spawn payload assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent plaintext context files may retain secrets, credentials, regulated personal data, or sensitive business material.

Mitigation: Avoid using this skill for sensitive material unless retention, redaction, and path-containment safeguards are added first.

Risk: A helper can append content to any writable file path it is given.

Mitigation: Review target context paths before use and restrict execution to trusted workspaces with appropriate file permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devymex/skills/safe-subagent-spawn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON spawn payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and appends plaintext context files that preserve full subagent interaction history.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
