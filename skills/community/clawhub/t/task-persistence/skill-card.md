## Description:

Task continuity, session snapshots, and gateway restart recovery for long-running tasks, interrupted sessions, and user status or recovery requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangdaowan](https://clawhub.ai/user/yangdaowan)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register long-running tasks, inspect active work, recover interrupted tasks after gateway restarts, and restore session context from persisted snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores task metadata, session snapshots, and conversation-related state as plaintext files in the workspace.

Mitigation: Use it only in workspaces where plaintext persistence is acceptable, avoid recording secrets in prompts or task metadata, and restrict workspace file permissions.

Risk: Unsafe task or session identifiers may allow JSON files outside intended folders to be read or overwritten.

Mitigation: Do not pass user-controlled or untrusted task IDs or session IDs until strict identifier validation and path containment checks are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangdaowan/skills/task-persistence)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yangdaowan)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates plaintext task, gateway state, and session snapshot records in the configured workspace when its commands are run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
