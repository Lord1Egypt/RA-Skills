## Description:

Helps an agent query Qunar travel information for flights, hotels, scenic tickets, and train tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellllll0world](https://clawhub.ai/user/hellllll0world)

### License/Terms of Use:


## Use Case:

External users and travel-support agents use this skill to collect trip parameters, call Qunar travel APIs, and summarize flight, hotel, scenic-ticket, or train-ticket results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Qunar API key can be sent to a caller-supplied API endpoint.

Mitigation: Restrict API requests to known Qunar HTTPS domains and avoid arbitrary or third-party endpoint URLs.

Risk: Travel prices, availability, and API parameters may be stale or incorrect if the endpoint or Qunar documentation has changed.

Mitigation: Confirm endpoint URLs and required parameters against current Qunar developer documentation before relying on results.

## Reference(s):

- [Qunar API Reference](references/api_reference.md)
- [Qunar Open Platform](http://open.qunar.com)
- [Qunar Developer Documentation](http://open.qunar.com/developer/doc)
- [ClawHub Skill Page](https://clawhub.ai/hellllll0world/skills/qunar-travel-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON command output from the query script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports list, detail, and conversation-style result presentations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
