## Description: <br>
Distill a teammate into an AI Skill by collecting Slack, Teams, GitHub, email, and document evidence, then generating a Work Skill and five-layer Persona that can evolve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myclaw-ai](https://clawhub.ai/user/myclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, team leads, and developers use this skill to preserve coworker knowledge, review style, decision patterns, and communication habits as reusable teammate skills. It supports creating, updating, comparing, exporting, and smoke-testing generated teammate profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect, persist, export, and impersonate sensitive coworker communications. <br>
Mitigation: Install only with organizational approval and, where required, teammate consent; avoid private messages and regulated, HR, or customer data. <br>
Risk: Slack and GitHub collectors may gather more information than intended if scopes and collection boundaries are broad. <br>
Mitigation: Use least-privilege Slack and GitHub scopes, narrow channel, repository, and date selections, and review collected material before generation. <br>
Risk: Generated teammate skills may include personal data or inaccurate behavioral claims. <br>
Mitigation: Review generated SKILL.md files before global installation and run the privacy scan before sharing or exporting. <br>
Risk: Export packages can include raw source knowledge when explicitly requested. <br>
Mitigation: Do not use --include-knowledge unless raw source data is intentionally being packaged for an approved recipient. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/myclaw-ai/teammate-skill) <br>
- [Publisher profile](https://clawhub.ai/user/myclaw-ai) <br>
- [README](artifact/README.md) <br>
- [Installation and setup guide](artifact/INSTALL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated teammate packages can include SKILL.md, work.md, persona.md, meta.json, version history, and optional source knowledge files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and CHANGELOG, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
