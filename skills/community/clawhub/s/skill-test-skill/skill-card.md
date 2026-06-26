## Description: <br>
Tests and scores Agent Skills against the Agent Skills specification, producing a compliance score and prioritized improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngfreefjs](https://clawhub.ai/user/youngfreefjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to audit an Agent Skill directory, SKILL.md file, or referenced repository for specification compliance, scoring, and actionable quality improvements. It supports English and Chinese Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to read every file in a provided skill directory, which can expose secrets or unrelated proprietary content if the user points it at a broad workspace. <br>
Mitigation: Provide a narrow skill folder or sanitized copy, and avoid directories containing API keys, credentials, private configuration, or unrelated proprietary files. <br>


## Reference(s): <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [anthropics/skills repository](https://github.com/anthropics/skills) <br>
- [Anthropic skill-creator guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) <br>
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills) <br>
- [Specification Summary](references/spec-summary.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with scoring tables, findings, improvement suggestions, and checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report language follows the user's request when English or Chinese is detected.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
