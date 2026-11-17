## Description:

Quote Swarm guides agents through smart-home quotation workflows, including floor-plan parsing, device identification, proposal design, quote generation, and handoff packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home solution designers use this skill to coordinate a full quotation workflow from floor-plan inputs to device counts, layout and wiring deliverables, and an HTML quote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes persistent local file creation while its declared permissions only mention file-read and network access.

Mitigation: Review installation permissions and either grant narrowly scoped write access for the expected task directories or remove automatic file-creation steps.

Risk: Customer names are used in path construction for task and quote files.

Mitigation: Sanitize customer-provided names before using them in paths and reject path separators or traversal sequences.

Risk: Broad activation triggers may cause the skill to run in unrelated quotation or floor-plan conversations.

Mitigation: Narrow activation wording and require explicit confirmation before reading customer documents or creating local records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoshung1981888/skills/quote-swarm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated file specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes HTML quote, PNG layout and wiring diagrams, JSON device-list outputs, and local task records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
