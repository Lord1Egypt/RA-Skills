## Description:

Find jobs that fit the user, apply to their matches and follow their applications with Tolta, an AI job application agent that applies on employers' own career forms. Use when the user asks for job matches or job openings, wants to apply to a job, or asks where their job applications stand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wassim](https://clawhub.ai/user/wassim)

### License/Terms of Use:

MIT

## Use Case:

External job seekers use the skill to find relevant openings, review fit and role details, apply to selected matches, and track application status through Tolta.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes a low-level agency concern and incomplete scan evidence because one referenced local path was unresolved.

Mitigation: Review the unresolved reference and skill behavior before enabling application actions.

Risk: Applying to a match sends a real application to an employer, or a draft when application review is enabled.

Mitigation: Call apply_to_match only after the user explicitly asks to apply to that job; direct unanswered application questions to Tolta.

## Reference(s):

- [How Tolta works](https://tolta.ai/how-it-works)
- [Using Tolta from AI assistants](https://tolta.ai/ai-assistants)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Text and Markdown, including shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job matches, role details, application updates, and status summaries; application submission is performed only when explicitly requested]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
