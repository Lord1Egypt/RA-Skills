## Description: <br>
Sop Extractor helps users turn SOP documents or structured interviews into reusable AI skill workflow documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business teams use Sop Extractor to capture repeatable finance, HR, operations, or project workflows through document parsing or guided questions and turn them into reusable AI skill instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may persist workflow instructions that include credential handling or business-system actions. <br>
Mitigation: Review each generated skill before saving or running it, and require explicit approval before credential writes, package installs, or business-system actions. <br>
Risk: Users may be asked for sensitive credentials while configuring generated workflows. <br>
Mitigation: Avoid real passwords, broad database credentials, and webhook URLs unless clearly needed; prefer scoped app tokens or read-only accounts. <br>
Risk: Broad or ambiguous trigger phrases could cause a generated workflow to run in the wrong context. <br>
Mitigation: Keep generated trigger phrases narrow and unambiguous, and require human confirmation for approval or amount-related actions. <br>


## Reference(s): <br>
- [Dialogue Examples](references/dialogue-examples.md) <br>
- [Questioning Guide](references/questioning-guide.md) <br>
- [SOP Parsing Guide](references/sop-parsing-guide.md) <br>
- [Tool Discovery Guide](references/tool-discovery-guide.md) <br>
- [Skill Template](references/skill-template.md) <br>
- [Credential Setup Guide](references/credential-setup-guide.md) <br>
- [Expense Approval Skill Example](references/examples/expense-approval-skill.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/sop-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Natural-language dialogue plus generated Markdown skill documents with optional shell commands or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflow documents should be reviewed and confirmed by the user before saving, running, or configuring dependencies.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
