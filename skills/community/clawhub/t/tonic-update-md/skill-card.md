## Description:

Create or update project documentation in Markdown for new project doc sets, deploy or feature changes, and standard file map conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonylnng](https://clawhub.ai/user/tonylnng)

### License/Terms of Use:


## Use Case:

Developers and project-maintenance agents use Update MD to create or update concise Markdown documentation sets, including project overviews, deployment notes, app specs, database docs, and release history after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project documentation can accidentally expose passwords, tokens, private keys, or sensitive host details.

Mitigation: Keep secrets and sensitive host details out of shared Markdown and review generated documentation before publishing.

Risk: Documentation navigation updates can broaden an agent's context beyond the intended project documents.

Mitigation: Review any AGENTS.md doc-map update so it stays limited to documentation navigation.

Risk: Stale or overly broad documentation changes can mislead future project work.

Mitigation: Apply the skill's update rules, edit only affected documents, and review documentation diffs after deploys or feature changes.

## Reference(s):

- [doc-templates.md](references/doc-templates.md)
- [ClawHub skill page](https://clawhub.ai/tonylnng/skills/tonic-update-md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documents and concise guidance, with optional inline shell-command examples in deployment templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; outputs are documentation structure, templates, update rules, and maintenance guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
