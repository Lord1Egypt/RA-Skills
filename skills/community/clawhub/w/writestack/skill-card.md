## Description:

Helps Substack creators draft, schedule, and review Notes and articles through their WriteStack account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orelsprojects](https://clawhub.ai/user/orelsprojects)

### License/Terms of Use:

MIT-0

## Use Case:

Substack creators use this skill to draft and manage Notes and articles, plan publication schedules, and review their own posting performance using WriteStack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Content may be scheduled or published at an unintended time.

Mitigation: Review the content and proposed schedule, and require the user's clear confirmation before scheduling or publishing.

Risk: A connected WriteStack account remains accessible through the OAuth connection.

Mitigation: Use the account sign-in flow rather than sharing credentials in chat; remove or revoke the connection when no longer needed.

Risk: Pushing an article may overwrite an existing Substack draft.

Mitigation: Explain the overwrite before pushing and confirm the intended article with the user.

## Reference(s):

- [WriteStack](https://www.writestack.io)
- [WriteStack skill on ClawHub](https://clawhub.ai/orelsprojects/skills/writestack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Conversational text and Markdown drafts, with connection commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts, queue summaries, scheduling guidance, and performance summaries draw on the user's connected account.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
