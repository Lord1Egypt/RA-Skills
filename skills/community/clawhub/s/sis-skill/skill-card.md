## Description: <br>
Adds equilibrium-constrained symbolic reasoning to OpenClaw assistants, with validation, adaptive balancing, and local vault persistence helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Architect-SIS](https://clawhub.ai/user/Architect-SIS) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to structure analyses, state updates, and tradeoff decisions around balance checks and symbolic operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hard-coded /home/claude/sis Python import path could cause the skill to load unreviewed local code. <br>
Mitigation: Remove the sys.path change and use package-relative imports from the bundled files before deployment. <br>
Risk: The equilibrium checks may be mistaken for a safety guarantee. <br>
Mitigation: Treat the checks as advisory reasoning support and review outputs before relying on them. <br>
Risk: Vault features can persist local symbol records. <br>
Mitigation: Enable file persistence only for data that is acceptable to store locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Architect-SIS/sis-skill) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with inline code snippets and Python library behavior.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist symbol records locally when vault features are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
