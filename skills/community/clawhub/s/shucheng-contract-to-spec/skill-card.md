## Description:

将合同文件转换为需求规格说明书，生成系统架构图、功能原型图说明和格式化 Word 文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lan2898408767](https://clawhub.ai/user/lan2898408767)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn a local project contract DOCX into a standardized Chinese requirements specification document with a cover page, revision record, table of contents, structured requirements sections, and generated architecture imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the main contract-to-spec output is largely hardcoded rather than actually derived from contract contents.

Mitigation: Run only on non-sensitive contract copies and manually verify all generated DOCX content before using it for client, procurement, or compliance deliverables.

Risk: The artifact hardcodes business values such as contract number, client, and contractor while deriving the project name primarily from the filename.

Mitigation: Confirm or replace all business identifiers and project details in the generated document before distribution.

Risk: The skill writes local files to the desktop and invokes Playwright through npx for browser screenshots.

Mitigation: Review input and output paths before execution and use a controlled local dependency setup with pinned browser tooling where possible.

## Reference(s):

- [需求规格说明书格式规范](references/format_spec.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [DOCX document with generated HTML and PNG diagram assets, plus agent guidance for running the workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the final requirements specification to the user's desktop using the naming pattern '{project_name} 需求规格说明书_v6.0.docx'.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
