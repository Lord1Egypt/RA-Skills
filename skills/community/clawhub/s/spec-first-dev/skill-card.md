## Description:

Guides agents through a spec-first development workflow that creates a comprehensive SPEC.md before implementation and requires user approval before coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevdogg102396-afk](https://clawhub.ai/user/kevdogg102396-afk)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill at the start of non-trivial build work to clarify intent, inspect the existing codebase, draft a SPEC.md, and wait for explicit approval before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a repository by writing SPEC.md before a user has explicitly confirmed file creation.

Mitigation: Review the generated SPEC.md before continuing and prefer versions or operating procedures that check for existing files before writing.

Risk: The skill requests broad shell access for a workflow that mainly needs repository discovery.

Mitigation: Run it in a trusted workspace and restrict command execution to read-only discovery commands where possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown file plus conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SPEC.md in the project root and may optionally produce SPEC_APPROVED.md after review.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
