## Description:

Publish, edit, and manage Substack posts for the Alternative Partners publication via Substack's internal REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breynol01](https://clawhub.ai/user/breynol01)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to create drafts, publish posts, update existing posts, and retrieve post IDs for the Alternative Partners Substack publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or edit live public Substack posts.

Mitigation: Require explicit user confirmation before publishing new posts or editing live posts.

Risk: The skill relies on a long-lived Substack browser session cookie.

Mitigation: Treat SUBSTACK_SID as a sensitive account credential, keep it out of chat logs and shell history where possible, and rotate it if exposed.

Risk: The skill is scoped to the Alternative Partners Substack publication.

Mitigation: Install only when the agent is intended to manage that publication.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in Substack API calls that create drafts, publish web posts without email blasts, edit live posts, or fetch post metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
