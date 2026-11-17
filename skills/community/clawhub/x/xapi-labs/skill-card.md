## Description:

Use xapi CLI to access real-time external data including Twitter/X profiles, tweets, timelines, crypto token prices and metadata, web search, news, and AI text processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glacier-luo](https://clawhub.ai/user/glacier-luo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call xapi from the command line for real-time social, crypto, web, news, AI text, and third-party API data. The skill guides agents to discover actions, inspect schemas, pass JSON inputs, and handle authentication or OAuth requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route user data to external APIs and AI text services.

Mitigation: Avoid sending sensitive documents or secrets unless external transmission is intended and approved.

Risk: OAuth-backed actions can authorize write operations such as posting tweets.

Mitigation: Require explicit user confirmation before OAuth binding or any write-capable action.

Risk: The npx entrypoint may execute an unpinned package version.

Mitigation: Pin or preinstall a reviewed xapi-to version in restricted environments.

Risk: API keys, top-up URLs, and ~/.xapi/config.json contain sensitive credentials.

Mitigation: Keep these values out of logs and share them only with approved xapi.to domains.

## Reference(s):

- [xAPI homepage](https://xapi.to)
- [ClawHub skill page](https://clawhub.ai/glacier-luo/skills/xapi-labs)
- [ClawHub publisher profile](https://clawhub.ai/user/glacier-luo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command inputs or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and an XAPI_API_KEY or xapi account configuration; xapi command output is JSON by default.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
