## Description:

Upgrade OpenClaw and comprehensively discover new features, configuration options, hooks, and improvements relevant to the user's setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decentraliser](https://clawhub.ai/user/decentraliser)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to update a local OpenClaw installation, review relevant changelog and configuration changes, audit hooks and doctor recommendations, and apply selected improvements after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the local OpenClaw installation during an update.

Mitigation: Invoke it only when an OpenClaw update is intended, and review the generated report before approving any follow-up changes.

Risk: Configured external sub-agent models may receive gateway configuration data.

Mitigation: Use a trusted model provider and redact sensitive gateway configuration before allowing external model use.

Risk: A dirty OpenClaw working tree may be stashed before update and require cleanup if the run is interrupted.

Mitigation: Check `git stash list` in the OpenClaw repository after an interrupted or declined run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/decentraliser/skills/upgrade-openclaw)
- [Publisher profile](https://clawhub.ai/user/decentraliser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with shell commands, tables, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before applying configuration, hook, or skill changes.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
