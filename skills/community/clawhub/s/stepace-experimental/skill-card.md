## Description:

Generate AI music on your Android phone via the StepAce Experimental app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckadirt](https://clawhub.ai/user/ckadirt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent queue or schedule AI-generated music through the StepAce Experimental Android app, including prompts with optional lyrics, BPM, key, duration, vocal language, and time signature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's music prompt and StepAce pairing token to an external bridge endpoint.

Mitigation: Install only if you trust the StepAce Experimental bridge operator, and avoid sending sensitive lyrics or private text in prompts.

Risk: Ambiguous music or scheduling requests could queue unwanted generation on the user's phone.

Mitigation: Confirm ambiguous requests before queuing music, especially scheduled requests that depend on a date, time, or timezone.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckadirt/skills/stepace-experimental)
- [StepAce Homepage](https://cronicaia.com)
- [OpenClaw Bridge Queue Endpoint](https://openclaw-bridge.torrico-villanueva-cesar-kadir.workers.dev/openclaw/queue)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown or plain text with JSON payloads and curl shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a STEPACE_TOKEN pairing token and may include a scheduledAt timestamp in Unix milliseconds.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
