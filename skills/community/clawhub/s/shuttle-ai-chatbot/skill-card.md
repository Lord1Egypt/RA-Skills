## Description:

Shuttle AI Chatbot is a CLI skill that sends single or batch queries to a configured Shuttle AI /chat_direct endpoint and returns the response as JSON or plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sean810720](https://clawhub.ai/user/sean810720)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operational users can use this skill to query a trusted local Shuttle AI service for product specifications, product comparisons, and batch lookup workflows. It is intended for environments where the configured backend endpoint is approved for the submitted prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted query text, batch files, endpoint URLs, or language values could cause unintended local shell command execution in this version.

Mitigation: Install only in trusted environments, pass only trusted inputs, and restrict URL and language values until the CLI uses safer process invocation and input validation.

Risk: Prompts are sent to the configured Shuttle AI endpoint and may be unsuitable for sensitive data unless that backend is approved.

Mitigation: Use only trusted Shuttle AI endpoints and avoid sensitive prompts unless the backend is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sean810720/skills/shuttle-ai-chatbot)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON objects or plain text responses printed by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the query, response, elapsed time, timestamp, endpoint URL, and session ID when JSON output is selected.]

## Skill Version(s):

2.0.1 (source: server release metadata, package.json, skill.json, SKILL.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
