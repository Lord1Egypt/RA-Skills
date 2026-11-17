## Description:

Captures feature and bug requests as sanitized GitLab issues during planning meetings, only when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrowgmbh](https://clawhub.ai/user/xrowgmbh)

### License/Terms of Use:

MIT-0

## Use Case:

Planning meeting participants use this skill to turn explicitly requested feature and bugfix discussions into sanitized, confidential GitLab issues. It records issues only; implementation and other development work require a separate request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required English for authored GitLab content may not fit every meeting team's workflow.

Mitigation: Confirm that English issue content is suitable for the team before using the skill.

Risk: The security scan was partial because some local path-like references could not be resolved.

Mitigation: Review the unresolved references and assess the skill before deployment.

Risk: Meeting material could disclose confidential details if sanitization misses identifying information or secrets.

Mitigation: Inspect the complete issue payload and attachments, remove identifiers and secrets, and omit content that cannot be safely sanitized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-meeting-assistant)
- [xrowgmbh publisher profile](https://clawhub.ai/user/xrowgmbh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise conversational replies and English GitLab issue titles and descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Issue content is sanitized; issues are created as confidential.]

## Skill Version(s):

1.147.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
