## Description:

Analyze URLs, YouTube videos, tweets, or text for quality, bias, and reliability using the Vajra API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minhyeong112](https://clawhub.ai/user/minhyeong112)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send public URLs or non-sensitive text to Vajra for reliability, bias, quality, takeaway, warning, and verdict summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs or text are transmitted to Vajra and analysis reports receive public permalinks.

Mitigation: Use the skill only for public URLs or non-sensitive text, and avoid private, proprietary, or personally identifiable content.

Risk: The broad trigger language could cause content to be sent for analysis when a user only wanted local discussion.

Mitigation: Confirm before sending user-provided content to Vajra, especially when the content is not already public.

Risk: Interpolating user text directly into the documented curl JSON payload can break JSON structure or create command-line handling issues.

Mitigation: Submit content through a JSON serializer or safely piped data instead of manually interpolating untrusted text into a shell command.

## Reference(s):

- [Vajra ClawHub release](https://clawhub.ai/minhyeong112/skills/vajra)
- [Vajra service](https://www.vajra.to)
- [Vajra dashboard](https://www.vajra.to/dashboard)
- [Vajra analyze API endpoint](https://www.vajra.to/api/analyze)
- [Humanity Labs](https://humanitylabs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with optional JSON API response fields and permalink]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VAJRA_API_KEY; raw text input is limited to 50,000 characters according to the skill documentation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
