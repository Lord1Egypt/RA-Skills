## Description: <br>
Guides agents through updating OpenClaw documentation based on code changes, including diff analysis, source-to-doc mapping, documentation edits, scaffolding, and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frisky1985](https://clawhub.ai/user/frisky1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and documentation reviewers use this skill to identify documentation affected by code changes, update existing pages, scaffold new docs, and validate formatting and links before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repository changes and modify documentation files. <br>
Mitigation: Use it only in repositories where git and file access are acceptable, and review proposed documentation edits before approval. <br>
Risk: Documentation updates may introduce inaccurate or misleading guidance if code behavior is misunderstood. <br>
Mitigation: Validate frontmatter, links, formatting, examples, and alignment with current code behavior before committing changes. <br>


## Reference(s): <br>
- [Code to Documentation Mapping](references/CODE-TO-DOCS-MAPPING.md) <br>
- [Documentation Conventions](references/DOC-CONVENTIONS.md) <br>
- [API Reference Template](assets/api-reference-template.md) <br>
- [Guide Template](assets/guide-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, checklists, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create documentation files and validation steps based on repository diffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
