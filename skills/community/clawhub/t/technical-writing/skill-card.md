## Description: <br>
Activate this skill whenever a user asks to write, structure, or improve developer documentation across README files, API documentation, Architecture Decision Records, RFCs, changelogs, runbooks, diagram-as-code, style guides, documentation site generators, docs-as-code CI workflows, and code examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royhk920](https://clawhub.ai/user/royhk920) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and documentation maintainers use this skill to plan, draft, improve, and standardize developer documentation for projects, APIs, operations, and architecture decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example installer and runbook commands may be copied into real projects without enough verification. <br>
Mitigation: Replace curl-to-shell installers with pinned, verified installation steps and review every command before reuse. <br>
Risk: Runbook examples include commands that can restart services or alter production state. <br>
Mitigation: Treat remediation commands as placeholders requiring explicit approval, impact checks, validation, and rollback planning. <br>
Risk: Generated documentation can become inaccurate if templates are reused without project-specific review. <br>
Mitigation: Review generated documentation against the target project, update placeholders, and validate examples before publication. <br>


## Reference(s): <br>
- [Technical Writing Style Guide](references/writing-style-guide.md) <br>
- [Mermaid Diagram Cheatsheet](references/mermaid-cheatsheet.md) <br>
- [ADR Template](examples/adr-template.md) <br>
- [Runbook Template](examples/runbook-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/royhk920/technical-writing) <br>
- [Publisher Profile](https://clawhub.ai/user/royhk920) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with prose, templates, tables, code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable documentation templates and a scaffold script for creating documentation project structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
