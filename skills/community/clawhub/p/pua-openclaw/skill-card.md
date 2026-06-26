## Description: <br>
Pua is an instruction-only pressure-coaching skill that pushes an agent toward exhaustive problem-solving, validation evidence, and changed approaches after frustration or repeated failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rorschachachxd](https://clawhub.ai/user/rorschachachxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Pua to make coding or troubleshooting agents take a more assertive, evidence-driven posture. It emphasizes validation commands, root-cause analysis, method switching after repeated failures, and structured failure reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate broadly in response to user frustration or repeated failures, which may make an agent's tone more aggressive than intended. <br>
Mitigation: Prefer explicit /pua activation, and keep normal safety, approval, and tone rules above the skill. <br>
Risk: The skill asks the agent to keep persistent cross-session behavior records in ~/.pua/evolution.md. <br>
Mitigation: Do not allow writes to ~/.pua/evolution.md unless persistent behavior records are intentionally desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rorschachachxd/pua-openclaw) <br>
- [Homepage](https://github.com/tanweai/pua) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional command and validation-output snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; may request validation evidence and structured failure reports.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, target metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
