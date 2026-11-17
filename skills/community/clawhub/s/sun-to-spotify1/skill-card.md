## Description:

Generate Sun audio and stream episodes to Spotify as a podcast using the `sun` CLI or HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbot001](https://clawhub.ai/user/sunbot001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate podcasts, audiobooks, or audio courses from a user prompt and publish the resulting episodes to Spotify. It guides authentication, job creation, incremental episode fetching, upload sequencing, and error handling for CLI and HTTP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a curl-to-bash installer path.

Mitigation: Prefer an isolated exact-version install with `uv tool` or `pipx`; review the installer before using curl-to-bash.

Risk: Authentication and token creation can expose sensitive credentials or full token secrets.

Mitigation: Have the user complete browser login directly, avoid pasting passwords or full tokens into agent chats or logs, and store tokens in an environment variable or secret manager.

Risk: The workflow can publish generated audio to the wrong Spotify destination.

Mitigation: Confirm the Spotify account, show creation choice, and target show before allowing uploads.

Risk: Using the wrong Sun API host can send requests or tokens to an unintended service.

Mitigation: Confirm the Sun API host before token creation or audio generation, especially when environment overrides are present.

## Reference(s):

- [Sun CLI Usage](artifact/cli-usage.md)
- [Sun Public HTTP API](artifact/http-api.md)
- [ClawHub skill page](https://clawhub.ai/sunbot001/skills/sun-to-spotify1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for authentication, polling, incremental downloads, Spotify upload sequencing, and user-facing error handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
