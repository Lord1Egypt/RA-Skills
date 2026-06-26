## Description: <br>
Analyzes customer-service messages with a local rule engine to classify sentiment, detect sensitive terms, flag escalation conditions, and recommend a reply tone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongfeng-wenfang](https://clawhub.ai/user/hongfeng-wenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer support agents and workflow developers use this skill to analyze customer messages, choose an appropriate response tone, and identify messages that may need escalation or human intervention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tracking feature stores customer message snippets in a shared temporary directory with weak session scoping and cleanup controls. <br>
Mitigation: Use the analyzer-only path for sensitive text, or modify tracking to store only derived scores in a private directory with restrictive permissions, validated session IDs, and automatic retention cleanup. <br>


## Reference(s): <br>
- [Reply Tone Guide](references/reply_tone.md) <br>
- [Emotion Tracking Mechanism](references/emotion_tracking.md) <br>
- [Capability Checklist](references/capability_checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hongfeng-wenfang/sentiment-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON sentiment results with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzer output includes sentiment, score, keywords, sensitive words, alert status, alert reason, reply tone, and input length; tracker output may also include escalation alert fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
