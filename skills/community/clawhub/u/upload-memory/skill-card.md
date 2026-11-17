## Description:

Upload Memory lets an agent recall and save durable user memories across AI agents through a shared cloud account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banlon](https://clawhub.ai/user/banlon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Upload Memory to give supported AI agents long-term memory, including recalling durable user facts at task start and saving new durable facts after interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically profiles the user and uploads durable memories to a cross-agent cloud store.

Mitigation: Review what is saved, avoid secrets and transient data, and confirm review, deletion, and token-revocation controls before deployment.

Risk: The first-run import behavior may read local Claude session history when no memories are available.

Mitigation: Require explicit user opt-in before importing session history and review extracted memories before upload.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/Banlon/upload-brain-marketplace/tree/main/plugins/upload-memory/skills/upload-memory)
- [ClawHub skill page](https://clawhub.ai/banlon/skills/upload-memory)
- [Upload.one registration page](https://upload.one/register.html?ref=DG5ZRF)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text memory facts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger recall and save commands that read or write cloud-backed memories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
