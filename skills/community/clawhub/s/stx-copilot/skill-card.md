## Description:

STX Copilot helps agents answer IBM Transformation Extender (WTX/ITX/Sterling TX) design, mapping, debugging, execution, and deployment questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoaibkhan](https://clawhub.ai/user/shoaibkhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill as IBM Transformation Extender guidance for type trees, map rules, Design Studio workflows, CLI execution, ACE integration, and financial message transformations such as SWIFT MT, ISO 20022, EDIFACT, COBOL copybook, and CSV mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace logging and WTX_DUMP_DATA examples can expose payment or customer data if enabled in production workflows.

Mitigation: Use those examples only with approval, redaction, restricted log access, and short retention; avoid enabling them on real payment or customer data.

Risk: The Launcher administration example includes an admin/secret credential pattern that could create weak administrative access if copied.

Mitigation: Replace sample credentials with organization-approved secrets and access controls before using any Launcher administration command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shoaibkhan/skills/stx-copilot)
- [Publisher GitHub profile](https://github.com/ShoaibKhan)
- [ACE / IIB Integration Reference](references/ace-integration.md)
- [STX Core Concepts Reference](references/core-concepts.md)
- [Debugging Reference](references/debugging.md)
- [Design Studio Workflow Reference](references/design-studio.md)
- [Execution Reference - CLI, Launcher, Deployment](references/execution.md)
- [Map Rules and Expressions Reference](references/expressions.md)
- [Data Formats Reference](references/formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline code, command examples, tables, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IBM Transformation Extender examples that must be reviewed before use with production payment or customer data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
