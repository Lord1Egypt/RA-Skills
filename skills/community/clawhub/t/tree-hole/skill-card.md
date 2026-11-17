## Description:

Anonymous story and confession submission to the community "tree hole" Feishu form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to submit stories, confessions, thoughts, or selected chat conversations anonymously to a community Feishu form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive stories or chat history to an external Feishu form.

Mitigation: Use only content the user explicitly wants submitted, manually select any chat history, and redact names, contact details, addresses, and other sensitive details before submission.

Risk: The workflow depends on installing and using the agent-browser skill to operate the web form.

Mitigation: Verify the agent-browser source and version before installation and review browser actions before final submission.

Risk: A login or identity collection prompt could undermine anonymous submission.

Mitigation: Stop submission if a login prompt appears and resolve the Feishu form identity-collection setting before retrying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/tree-hole)
- [Community Feishu submission form](https://ainewmedia.feishu.cn/share/base/form/shrcn1AeCLxzQdV15UaxAzu2L0e)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions are sent to an external Feishu form after user-provided or user-selected content is filled into the form.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
