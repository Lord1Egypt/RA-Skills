## Description:

Shorten URLs via TinyURL or Bitly API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to ask an agent for shortened URLs through TinyURL by default or Bitly when a Bitly token is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs are sent to third-party URL-shortening services.

Mitigation: Confirm users are comfortable sending URLs to TinyURL or Bitly and avoid URLs containing sensitive embedded data.

Risk: Bitly usage requires a BITLY_TOKEN environment variable.

Mitigation: Provide BITLY_TOKEN only through normal environment handling and avoid exposing it in prompts, logs, or shared command text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/url-shorten)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; Bitly use depends on BITLY_TOKEN, otherwise TinyURL is used.]

## Skill Version(s):

1.0.0 (source: server release metadata, published 2026-02-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
