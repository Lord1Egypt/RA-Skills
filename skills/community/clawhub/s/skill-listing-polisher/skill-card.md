## Description:

Improve a skill's public listing before publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyoiii](https://clawhub.ai/user/kyoiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill before publishing or updating a public ClawHub skill to tighten listing title, description, tags, changelog, and package contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested listing edits could remove useful context or understate package behavior.

Mitigation: Review the final title, description, tags, changelog, and package file list before publishing.

Risk: The bundled listing check can flag internal-looking names or sensitive strings but does not prove a package is disclosure-ready.

Mitigation: Use the check as a prompt for manual review and scan the skill before deployment.

## Reference(s):

- [Review Notes](references/review-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with concise review findings and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns trust issues, discoverability issues, and the smallest edit that improves both.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
