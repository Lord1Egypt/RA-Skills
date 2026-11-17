## Description:

A conversational requirement clarification tool with structured questioning and document generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers, product managers, and project teams use this skill to clarify project requirements through a structured dialogue and generate a completeness-scored requirement document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved requirement sessions and documents may contain confidential project details.

Mitigation: Store generated JSON only in approved workspaces and avoid entering secrets unless that storage location is acceptable.

Risk: Persistence writes to caller-supplied paths and can replace files at those paths.

Mitigation: Choose output paths deliberately and avoid reusing paths for files that should not be overwritten.

## Reference(s):

- [Requirement Guide on ClawHub](https://clawhub.ai/terr123123/skills/requirement-guide)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Conversational text and structured requirement documents, with optional JSON persistence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents include requirement elements and a completeness score.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
