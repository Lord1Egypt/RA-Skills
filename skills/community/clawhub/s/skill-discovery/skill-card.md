## Description: <br>
Discovers and recommends skills from user intent, searches matching registries, validates candidate quality, and returns a recommended skill for user-confirmed installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caocong1](https://clawhub.ai/user/caocong1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find relevant agent skills for tasks such as deployment, testing, documentation, data processing, security, and optimization. It returns a recommendation and installation command so the user can review the selected skill before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the skill can search external registries and has code paths that install or remove global skills. <br>
Mitigation: Use dry-run recommendation mode by default, review the exact skill name and source before installing, and avoid unattended install or remove paths unless the caller and registry results are trusted. <br>
Risk: Documentation and behavior may be inconsistent about whether installation happens automatically or only after confirmation. <br>
Mitigation: Treat returned install commands as proposals for user review and prefer the OpenClaw hook or explicit dry-run mode for normal use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caocong1/skill-discovery) <br>
- [Project Homepage](https://github.com/caocong1/skill-discovery) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured result objects with recommended install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected skill metadata, candidate lists, status fields, error codes, and dry-run installation guidance.] <br>

## Skill Version(s): <br>
2.2.1 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
