## Description: <br>
A Chinese-language safety review protocol for assessing AI agent skills before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xocio](https://clawhub.ai/user/xocio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review ClawHub, GitHub, or shared AI agent skills before installation. It helps structure source checks, risky-pattern review, permission analysis, risk grading, and a final review report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes sample dangerous commands and URLs for recognition during reviews. <br>
Mitigation: Treat those samples as examples to identify risky behavior, not as commands to execute. <br>
Risk: Using the checklist may involve inspecting files or network metadata from another skill under review. <br>
Mitigation: Limit inspection to the files, commands, and network access needed for the specific review, and avoid sensitive credential locations unless the user explicitly approves. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xocio/skill-vetter-zh) <br>
- [Publisher profile](https://clawhub.ai/user/xocio) <br>
- [Source project listed in README](https://clawhub.ai/spclaudehome/skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with checklist templates, report templates, and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language review workflow; examples should be treated as reference patterns, not commands to run automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
