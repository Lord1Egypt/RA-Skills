## Description: <br>
RiskBlind Radar proactively asks overlooked risk questions in AI conversations before users make plans, spend money, launch work, or commit to product assumptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryuutora1986](https://clawhub.ai/user/ryuutora1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, small-team leads, and AI-assistant power users use this skill to surface decision blind spots through concise follow-up questions about ROI, commitment risk, success criteria, assumptions, opportunity signals, and exit conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger keywords may cause occasional over-triggering or unnecessary follow-up questions. <br>
Mitigation: Tune the trigger words and disable templates that do not match the user's decision context. <br>
Risk: The optional observation log may retain notes about commitments or risk concerns across conversations. <br>
Mitigation: Keep the observation log disabled or periodically clear it when persistent risk notes are not desired. <br>
Risk: Decision-support questions can be incomplete or inappropriate for specialized legal, financial, medical, or safety-critical choices. <br>
Mitigation: Treat the output as prompting for reflection and use qualified review for high-stakes decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryuutora1986/riskblind-radar) <br>
- [Publisher profile](https://clawhub.ai/user/ryuutora1986) <br>
- [README](artifact/readme.md) <br>
- [Question templates](artifact/question_templates.md) <br>
- [Rules](artifact/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Conversational text and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask up to two proactive risk questions per substantive turn and may optionally use a Markdown observation log for risk tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
