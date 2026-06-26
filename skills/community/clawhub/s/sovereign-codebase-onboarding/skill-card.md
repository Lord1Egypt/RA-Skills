## Description: <br>
Codebase onboarding assistant that maps project architecture, identifies patterns, generates guides, and helps new developers understand any repository in minutes instead of days. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, tech leads, open source contributors, and AI agents use this skill to analyze unfamiliar repositories, map architecture, identify patterns and key files, and generate onboarding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad repository inspection may surface private source details, credentials, deployment configuration, or proprietary material in generated onboarding artifacts. <br>
Mitigation: Before running on private code, exclude .env files, secrets, credentials, keys, sensitive deployment configs, and proprietary material that should not be summarized. <br>
Risk: Generated architecture maps and onboarding guidance can be incomplete or outdated if the repository evidence is missing, stale, or too broad to inspect fully. <br>
Mitigation: Have a project maintainer review generated guides before using them for onboarding, audits, or implementation decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryudi84/sovereign-codebase-onboarding) <br>
- [Skill README](artifact/README.md) <br>
- [Usage examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with ASCII diagrams, tables, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content depends on repository access and should be reviewed for accuracy before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
