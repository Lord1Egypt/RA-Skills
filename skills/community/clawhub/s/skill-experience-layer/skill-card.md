## Description:

Adds pre-call experience checking, error-driven learning, and layered per-skill memory so agents can avoid repeated mistakes and improve over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jilanfang](https://clawhub.ai/user/jilanfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent, per-skill experience memory that checks prior lessons before skill use and records new mistakes after failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic changes to persistent agent memory may introduce incorrect, stale, or unwanted guidance.

Mitigation: Require review and approval before writing corrections, updating best practices, or applying any long-term memory change.

Risk: Repeated-error automation may invoke capability-evolver or propose broader memory updates without enough oversight.

Mitigation: Treat capability-evolver use and MEMORY.md changes as reviewed proposals, not automatic edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jilanfang/skills/skill-experience-layer)
- [Publisher profile](https://clawhub.ai/user/jilanfang)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent memory guidance and experience-file structures for agent workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
