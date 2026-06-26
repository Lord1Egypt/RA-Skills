## Description: <br>
L0-grade secure skill installation workflow for OpenClaw skills that guides duplicate checks, candidate search, security review, isolated installation, formal installation, and authorized whitelist updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage OpenClaw skill installation through a structured review flow before installing or changing persistent trust configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow exempts a hardcoded trusted author and skill list from normal risk review. <br>
Mitigation: Require clawhub inspect for every skill, including allowlisted authors, before installation. <br>
Risk: The workflow can make persistent allowBundled trust changes to OpenClaw configuration. <br>
Mitigation: Confirm the exact skill slug and obtain explicit user approval before editing allowBundled. <br>


## Reference(s): <br>
- [Skill Safe Install on ClawHub](https://clawhub.ai/halfmoon82/skill-safe-install-l0) <br>
- [halfmoon82 publisher profile](https://clawhub.ai/user/halfmoon82) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and step-by-step status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes explicit authorization language before allowBundled configuration changes.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
