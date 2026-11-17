## Description:

Extract and summarize public project and announcement information from Worktile shared pages without requiring login or accessing private data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and agents use this skill to extract titles, authors, update times, summaries, task groupings, status distributions, and resource links from publicly accessible Worktile project and announcement pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private team spaces or authenticated Worktile pages may expose non-public information if treated as public inputs.

Mitigation: Use the skill only with publicly accessible Worktile links unless separate approval grants access to private or authenticated pages.

Risk: Repeated collection of dynamically loaded pages can create unnecessary duplicate access.

Mitigation: Wait for rendering to complete, apply frequency control, and avoid repeat visits when collecting page content.

## Reference(s):

- [Worktile homepage](https://worktile.com/)
- [ClawHub Worktile skill page](https://clawhub.ai/codekungfu/skills/worktile)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summaries, statistics, and resource-link lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limited to publicly accessible Worktile pages and shared links.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
