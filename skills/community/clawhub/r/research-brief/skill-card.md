## Description:

Progressive research protocol for agents: write a stub file immediately, append findings incrementally, never save the write for last.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill when a research task should produce a persistent brief file. It directs the agent to create an initial Markdown stub before research and update the file as findings are gathered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages creating a file at the start of a research task, which may be undesirable when persistent output is not expected.

Mitigation: Use it for research-to-file workflows where creating a draft brief is intended, and confirm the destination file before starting.

Risk: An interrupted run can leave placeholder or partially updated sections in the brief.

Mitigation: Review the generated brief for remaining placeholders, source coverage, and recommendations before relying on it.

## Reference(s):

- [Research Brief ClawHub Page](https://clawhub.ai/nissan/skills/research-brief)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown research brief with incremental file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow starts with a stub file and updates sections as research findings and sources are gathered.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
