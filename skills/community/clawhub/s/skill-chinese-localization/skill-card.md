## Description: <br>
Translates ClawHub skill names and technical terms into plain Chinese so users can understand and match skills from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t22239007-max](https://clawhub.ai/user/t22239007-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and non-technical users use this skill to describe workflow needs in plain Chinese and receive understandable explanations of matching ClawHub skills before deciding whether to install one. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may route users toward installing other skills without enough scoping or security disclosure. <br>
Mitigation: Before installation, require the exact skill name or slug, publisher, version, permissions, review status, and a separate explicit yes/no approval. <br>
Risk: Skill explanations and matches may be incomplete or misleading because they are translation and routing aids rather than safety assessments. <br>
Mitigation: Treat recommendations as unverified guidance and review the target skill's publisher, release evidence, security status, and permissions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/t22239007-max/skill-chinese-localization) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [OpenClaw skill glossary](artifact/openclaw_skill_glossary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain Chinese explanations and structured skill-match guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend a matching ClawHub skill; installation should require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
