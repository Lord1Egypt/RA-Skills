## Description: <br>
Generate consistent, template-based Mermaid diagrams for technical content with support for 12 diagram types, automatic template selection, LLM-powered content generation, syntax validation, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical writers, and documentation teams use this skill to create consistent Mermaid diagrams for system architecture, workflows, timelines, UML-style models, state machines, and technical explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scripts can run unintended local shell commands when given crafted paths or filenames. <br>
Mitigation: Review before installing, use only trusted content and simple safe paths, and update scripts to call Mermaid CLI with argument arrays. <br>
Risk: Global Mermaid CLI installation can drift across environments. <br>
Mitigation: Prefer a pinned local Mermaid CLI dependency for repeatable rendering and easier dependency review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chunhualiao/skill-mermaid-diagrams) <br>
- [Mermaid syntax reference](references/mermaid-syntax.md) <br>
- [Mermaid documentation](https://mermaid.js.org/) <br>
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) <br>
- [Mermaid live editor](https://mermaid.live/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON content specifications, Mermaid source, SVG and PNG diagram files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated diagrams depend on user-provided or agent-generated placeholder content and Mermaid CLI rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
