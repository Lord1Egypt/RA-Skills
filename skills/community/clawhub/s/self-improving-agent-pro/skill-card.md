## Description: <br>
Local skill for capturing learnings, errors, corrections, and patterns to enable continuous agent improvement with structured insights, suggested rules, and batch summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to process local learning events, failures, corrections, and recurring patterns into structured insights and candidate rules for future agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged events may contain secrets, tokens, personal data, customer content, or untrusted instructions. <br>
Mitigation: Redact sensitive or untrusted content before sending events to the skill. <br>
Risk: Suggested rules may be incorrect or unsafe if added automatically to agent memory, configuration, databases, or multiple agents. <br>
Mitigation: Review every suggested_rule before applying or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennyzir/self-improving-agent-pro) <br>
- [Claw0x documentation](https://claw0x.com/docs) <br>
- [Claw0x self-improving agent](https://claw0x.com/skills/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON object with processed entries and an optional batch summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each entry may include severity, tags, an actionable insight, and a suggested rule; batch inputs may also return counts, recurring patterns, and recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
