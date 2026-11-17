## Description:

Use the Chanjing avatar API to create lip-sync videos by uploading source media, creating avatar tasks, and polling task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to create Chanjing lip-sync avatar videos from a source video and either text-to-speech input or an uploaded audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable Chanjing credentials and cached access tokens in a local credentials file.

Mitigation: Use a private configuration directory, restrict credentials.json to the local user account, and install only where the Chanjing credentials are trusted.

Risk: CHANJING_API_BASE can change the API endpoint used for credential and token requests.

Mitigation: Leave CHANJING_API_BASE unset unless intentionally using a trusted HTTPS endpoint.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON examples; runtime outputs include remote video URLs, task status, progress, and Chanjing file or task identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not auto-download generated videos by default; uses local Chanjing credentials and returns login guidance when credentials are missing or invalid.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
