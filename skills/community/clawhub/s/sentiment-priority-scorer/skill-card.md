## Description: <br>
Scores normalized real-estate leads using sentiment, urgency, intent, recency, and record type to produce deterministic priority rankings and P1-P3 buckets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Real-estate operations teams and agents use this skill to rank normalized leads for callback queues and follow-up triage without writing data or triggering outbound actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead text may contain sensitive business or customer information. <br>
Mitigation: Treat inputs as sensitive data and follow the deployment environment's data handling policy. <br>
Risk: Priority scores may be incorrect or may overstate the importance of a lead. <br>
Mitigation: Review generated priority scores before acting on them, especially before customer outreach. <br>
Risk: Recommended downstream skills may add summaries or action suggestions outside this skill's read-only scope. <br>
Mitigation: Review and approve downstream skills separately before using them in an automated chain. <br>


## Reference(s): <br>
- [Sentiment priority input schema](artifact/references/sentiment-priority-input.schema.json) <br>
- [Sentiment priority output schema](artifact/references/sentiment-priority-output.schema.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing scored leads with sentiment, priority score, priority bucket, and evidence tokens] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validates output against the bundled sentiment priority output schema and does not write data or send messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
