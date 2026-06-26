## Description: <br>
舆情风险预诊工具。单段文本快速风险评估，输出风险评分 (1-10)、风险等级 (蓝/黄/橙/红/黑)、传播力×危害力矩阵。适用于客服筛查、社交媒体预检。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhushanwei](https://clawhub.ai/user/zhushanwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer service, communications, and social media teams use this skill to screen a single text sample for public-opinion and reputation risk before deciding whether to monitor, escalate, or respond. It is best suited for quick triage rather than authoritative crisis response or full-network monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces heuristic reputation-risk scores that may be incomplete or wrong for high-impact incidents. <br>
Mitigation: Use the output as an initial screening aid and require human review before crisis-response, moderation, or escalation decisions. <br>
Risk: The artifact is intended for single-text triage, not broad monitoring or deep analysis. <br>
Mitigation: Limit use to quick checks of supplied text and pair it with appropriate monitoring, legal, communications, or domain review for broader cases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhushanwei/reputation-thermometer) <br>
- [examples.md](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON risk report with score, color-coded level, risk factors, industry classification, and response guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and analyzes one supplied text input at a time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
