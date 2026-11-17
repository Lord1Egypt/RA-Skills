## Description:

Answer questions from a persistent markdown knowledge wiki and file durable results back into the wiki when useful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teki-ai](https://clawhub.ai/user/teki-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and knowledge workers use this skill to query an existing personal or team markdown wiki, synthesize across related pages, cite wiki evidence, and save durable analysis when the result should remain reusable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify wiki content by creating analysis pages and updating index or log pages.

Mitigation: Use it with a git-backed or otherwise recoverable wiki and review file changes before keeping them.

Risk: A synthesized answer can be misleading when wiki evidence is incomplete, mixed, or uncertain.

Mitigation: Require citations to relevant wiki pages and preserve explicit uncertainty or disagreement in the answer.

## Reference(s):

- [Query Patterns](references/query-patterns.md)
- [Wiki Query ClawHub listing](https://clawhub.ai/teki-ai/skills/wiki-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown answers with wiki citations and optional markdown file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create reusable analysis pages and update index.md or log.md when the result has durable value.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
