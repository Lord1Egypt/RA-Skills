## Description: <br>
Create or update project documentation in Markdown for new doc sets, deploy or feature updates, and standard project file maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonylnng](https://clawhub.ai/user/tonylnng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use this skill to create and maintain structured Markdown project documentation, including overview, deployment, app, database, and history files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation can expose private keys, passwords, tokens, host details, or sensitive infrastructure information if users paste real secrets into templates. <br>
Mitigation: Use placeholders or secret-manager references for sensitive values and review Markdown changes before committing or sharing them. <br>
Risk: Documentation updates can become misleading if generated or changed files are not reviewed against the actual project state. <br>
Mitigation: Review generated AGENTS.md and project documentation changes before committing, and update only the files affected by the project change. <br>


## Reference(s): <br>
- [Update MD on ClawHub](https://clawhub.ai/tonylnng/tonic-update-md) <br>
- [Documentation Templates](references/doc-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown documents and update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Templates cover project overview, deployment, app, database, and history documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
