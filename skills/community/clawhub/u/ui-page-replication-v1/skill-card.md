## Description: <br>
High-fidelity UI page replication workflow for backend/admin systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhcong6](https://clawhub.ai/user/yhcong6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to replicate authorized backend/admin UI pages by collecting browser evidence, traversing interactions, and generating matching React/TypeScript implementation assets, mock data, API-shaped functions, styles, and verification notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser collection can capture sensitive admin information in screenshots, DOM snapshots, and interaction notes. <br>
Mitigation: Use the skill only on pages you own or are authorized to replicate, and prefer staging or sanitized data. <br>
Risk: Traversing create, update, delete, submit, or audit flows on a live system could cause unintended changes. <br>
Mitigation: Avoid confirming real mutating actions during exploration and implement mock-backed API functions first. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yhcong6/skills/ui-page-replication-v1) <br>
- [Skill Definition](SKILL.md) <br>
- [Reference Source README](references/source/README.md) <br>
- [Replication Prompt](references/source/prompt.ts) <br>
- [Configuration](references/source/config.ts) <br>
- [Page Schema Types](references/source/types.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, TypeScript interfaces, mock data, API layer notes, styles, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to capture Playwright screenshots, DOM snapshots, and interaction notes as supporting artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and references/source/config.ts) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
