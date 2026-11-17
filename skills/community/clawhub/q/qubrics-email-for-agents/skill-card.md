## Description:

Give OpenClaw agents a Qubrics inbox to receive, triage, route, reply to, and send email with owner approval and scoped credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to route agent email tasks to Qubrics workflows for inbox setup, mailbox triage, replies, and sending. It explains credential scopes and the required user approval boundaries for mailbox changes and outgoing messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended installer and source are not pinned to reviewed versions.

Mitigation: Review and pin the installer and skill source to versions approved for the deployment before setup.

Risk: Some local path-like references could not be resolved during security review, leaving partial reference coverage.

Mitigation: Review referenced local skills and paths before following those handoffs.

## Reference(s):

- [Qubrics skills project homepage](https://github.com/qubrics/skills)
- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-email-for-agents)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with routing tables, workflow steps, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-scope guidance and user-confirmation steps for writes and email sending.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
