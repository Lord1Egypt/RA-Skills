## Description:

An intent-clarification skill that turns vague requests into executable tasks by offering candidate directions, clarifying goals and constraints, and producing a ready-to-run prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

People who have a vague request or are unsure how to ask an AI use the skill to choose a direction, clarify goals, scope, output, and constraints, and receive a ready-to-run prompt that can point to a relevant YottaMeta skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing into an existing skill directory can overwrite this skill's files or remove development residues.

Mitigation: Choose one agent or directory, preview the target and changes, and pin a reviewed package version.

Risk: A generated global install command can affect multiple agents' skill directories.

Mitigation: Use a scoped agent or directory option and preview the installation before applying it.

Risk: Persistent activation and prompts that include language or memory-writing instructions may have effects beyond a single request.

Mitigation: Enable persistent activation only if wanted, and review the activation changes and generated prompts.

## Reference(s):

- [Scenario library](references/scenarios.md)
- [FAQ](references/faq.md)
- [Project homepage](https://github.com/YottaMeta/yotta-prompt)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Text or JSON containing candidate directions, clarifying questions, task descriptions, and ready-to-run prompt templates; optional installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate suggestions are typically 2–4 directions; JSON output is available for supported CLI commands.]

## Skill Version(s):

0.2.6 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
