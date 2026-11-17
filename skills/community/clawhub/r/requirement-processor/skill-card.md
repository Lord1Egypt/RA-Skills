## Description:

Requirement Processor helps agents structure new feature or change requests through clarification, project survey, requirements documentation, validation, planning, and iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn user requests into structured requirements documents, prioritized implementation phases, and follow-up validation questions before coding begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to persist project-derived experience notes inside the installed skill references directory, which can retain project information outside the current workspace.

Mitigation: Remove or override that persistence instruction before use, or require explicit approval and sanitization before any project information is saved there.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/requirement-processor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown requirements documents, planning notes, and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project requirements documents in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
