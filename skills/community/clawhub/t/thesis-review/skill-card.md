## Description:

Reviews academic degree theses with a structured evaluation framework for bachelor, master's, and PhD work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Academic reviewers, advisors, and students use this skill to extract thesis details, compare the work against evaluation criteria and recent literature context, and generate structured review comments. It supports thesis pre-review, blind-review simulation, batch review, and final review writeups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Thesis content may be confidential, and the workflow may search the web using topic keywords.

Mitigation: Confirm confidentiality requirements before use; ask the agent to avoid web search or use generalized keywords when thesis details should not leave the local context.

Risk: The skill may create a Word review file in the current working directory.

Mitigation: Run it from an appropriate workspace and review generated files before sharing them.

## Reference(s):

- [Thesis Review Skill Page](https://clawhub.ai/paudyyin/skills/thesis-review)
- [Review Patterns](references/review-patterns.md)
- [Review Templates](references/review-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown review comments with optional Python snippets and a generated Word document.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a .docx review file in the working directory.]

## Skill Version(s):

2.1.0 (source: server release metadata, package.json, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
