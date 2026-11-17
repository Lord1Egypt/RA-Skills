## Description:

Software Manager Skill helps agents provide product-manager support for requirements analysis, PRD writing, product planning, competitive analysis, Mermaid diagrams, DOCX/Markdown export, and interactive H5 prototype generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and product teams use this skill to structure product discovery conversations, compare solution options, draft PRDs, generate product diagrams, export documents, and create browser-viewable H5 prototypes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOCX export and Mermaid rendering involve local command execution and browser automation.

Mitigation: Review the skill before installing, run exports in a disposable or low-privilege environment, and avoid rendering Mermaid diagrams from untrusted sources.

Risk: Generated H5 prototypes may expose sensitive product details or user-provided sample data.

Mitigation: Do not include real credentials or confidential data in generated prototypes, and review prototype files before sharing or deploying them.

Risk: Dependency installation for document export can introduce global package or supply-chain exposure.

Mitigation: Pin and install dependencies locally where possible instead of relying on global npm or Python packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhongm/skills/software-manager-skill)
- [README](artifact/README.md)
- [PRD template](artifact/references/prd-template.md)
- [PM framework](artifact/references/pm-framework.md)
- [Mermaid guide](artifact/references/mermaid-guide.md)
- [Agile development](artifact/references/agile-dev.md)
- [Atlassian Agile](https://www.atlassian.com/software-development-lifecycle)
- [Scrum Guide](https://www.scrumguides.org/)
- [Mermaid Documentation](https://mermaid.js.org/)
- [Tailwind CSS Chinese Documentation](https://www.tailwindcss.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tables, Mermaid code blocks, export commands, and optional HTML/CSS/JavaScript prototype files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Markdown or DOCX PRD exports and single-file H5 prototypes when requested by the user.]

## Skill Version(s):

2.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
