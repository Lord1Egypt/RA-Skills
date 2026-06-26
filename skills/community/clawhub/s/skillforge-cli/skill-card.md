## Description: <br>
SkillForge generates and audits OpenClaw agent skills from natural language, with template-based generation and optional AI-powered quality assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadoprizm](https://clawhub.ai/user/shadoprizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use SkillForge to scaffold OpenClaw skills from descriptions, audit existing skill directories, and optionally publish approved skills to ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys may be stored locally in plaintext. <br>
Mitigation: Treat stored keys as sensitive credentials, avoid sharing the local configuration directory, and rotate keys if exposure is suspected. <br>
Risk: Pro mode can send audited skill contents to the selected AI provider. <br>
Mitigation: Audit only intended skill directories and exclude secrets, .env files, private keys, credentials, and unrelated private source material. <br>
Risk: The skill can publish generated or existing skills to ClawHub. <br>
Mitigation: Require explicit operator approval before any publish command and review generated skill files before release. <br>


## Reference(s): <br>
- [SkillForge ClawHub listing](https://clawhub.ai/shadoprizm/skillforge-cli) <br>
- [SkillForge repository declared in artifact metadata](https://github.com/shadoprizm/skillforge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, tables, generated skill files, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pro mode may send skill contents to the operator-selected AI provider; publishing commands require explicit operator approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact skill.json lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
