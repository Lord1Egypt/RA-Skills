## Description: <br>
Thinking-Claude inspired comprehensive thinking protocol with Verification Protocol and Confidence Scoring for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leezongdai](https://clawhub.ai/user/leezongdai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add a structured reasoning, verification, and confidence-reporting protocol to OpenClaw agents. It is intended for broad task handling where clearer analysis, uncertainty marking, and final-response checks are desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may influence most agent responses, including tasks where this reasoning style is not desired. <br>
Mitigation: Install only for agents that should consistently use this protocol, and review the activation wording before deployment. <br>
Risk: Required thinking blocks and confidence percentages may expose internal analysis style or be mistaken for calibrated certainty. <br>
Mitigation: Adapt the output policy to the host agent and treat confidence scores as qualitative unless separately validated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leezongdai/thinking) <br>
- [Thinking-Claude project](https://github.com/richards199999/Thinking-Claude) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with optional thinking code blocks, confidence assessments, and uncertainty tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May increase response length and influence the agent's reasoning and response structure across many task types.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence, SKILL.md frontmatter, and changelog; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
