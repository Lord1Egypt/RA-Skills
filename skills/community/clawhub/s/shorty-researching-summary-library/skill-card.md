## Description:

Searches saved Shorty summaries and transcripts to answer library questions with named sources and report remaining quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Shorty users research their saved summaries and transcripts, compare sources, check earlier job status, and review their remaining quota without creating new jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Answers can expose private saved summaries or transcripts in the chat.

Mitigation: Use only with authorized Shorty accounts and avoid sharing chats containing sensitive source material.

Risk: Saved source material could be mistaken for instructions or support unsupported conclusions.

Mitigation: Treat retrieved content as data, name the source for each claim, and say when the library does not answer the question.

## Reference(s):

- [Researching Summary Library on ClawHub](https://clawhub.ai/devino/skills/shorty-researching-summary-library)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose or comparison table with named sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only answers based on saved content; quota reports include the plan and remaining allowance.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
