## Description:

Analyzes customer-service messages for sentiment, sensitive words, escalation alerts, and recommended reply tone using local rule-based scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongfeng-wenfang](https://clawhub.ai/user/hongfeng-wenfang)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-support teams and developers use this skill to classify customer-message sentiment, detect sensitive terms, identify worsening conversation trends, and choose an appropriate response tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer-message excerpts may be written to an unsafe temporary tracking path.

Mitigation: Use a private directory with restrictive permissions, store only minimal derived sentiment data, and define retention and deletion behavior before use with real customer data.

Risk: Session IDs control tracking file paths.

Mitigation: Validate and constrain session IDs before using the tracking script.

Risk: The cleanup example uses raw file deletion.

Mitigation: Replace it with a safer deletion path that only removes validated session-tracking files.

## Reference(s):

- [Sentiment Analyzer ClawHub Page](https://clawhub.ai/hongfeng-wenfang/skills/sentiment-analyzer)
- [Emotion Tracking Mechanism](references/emotion_tracking.md)
- [Reply Tone Guide](references/reply_tone.md)
- [Capability Checklist](references/capability_checklist.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON sentiment analysis results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include sentiment label, score, keywords, sensitive-word matches, alert flags, alert reason, reply tone, and optional escalation tracking metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
