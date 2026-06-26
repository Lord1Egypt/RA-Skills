## Description: <br>
AI Agent Skill decision engine that helps users find, evaluate, and install skills with quality and safety scoring personalized to platform, region, budget, and skill level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smilelight](https://clawhub.ai/user/smilelight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to request personalized skill recommendations, compare alternatives, and retrieve install commands for tasks across ClawHub and GitHub skill catalogs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill recommendation queries are sent to skillscope.cn and may disclose task details. <br>
Mitigation: Avoid confidential task details when requesting recommendations. <br>
Risk: Recommended install commands may install third-party skills selected by an external service. <br>
Mitigation: Inspect the recommended skill and install command before running it. <br>


## Reference(s): <br>
- [SkillScope homepage](https://skillscope.cn) <br>
- [SkillScope API base](https://skillscope.cn/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/smilelight/skillscope) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with API examples and install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommendations, alternatives, scores, reasons, and install commands returned from the external SkillScope API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
