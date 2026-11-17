## Description:

Control Sony Bravia TV power, volume, apps, playback, and remote navigation over a local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssupppp](https://clawhub.ai/user/ssupppp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to let an agent control a Sony Bravia TV on the same local network, including power, volume, app launch, playback, status, and remote-button navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a real TV using a reusable local credential.

Mitigation: Use it only on a trusted local network, choose a strong TV PSK, and rotate the PSK if the .env file or local network traffic may have been exposed.

Risk: The generated .env file can contain the TV IP address, PSK, and MAC address.

Mitigation: Keep the .env file private and out of backups or source control.

Risk: Ambiguous media requests such as play or pause could unexpectedly control the TV.

Mitigation: Prefer explicit TV-related commands before sending playback or navigation actions.

## Reference(s):

- [Sony Bravia Known App URIs](references/app-uris.md)
- [ClawHub Skill Page](https://clawhub.ai/ssupppp/skills/sony-bravia-tv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and brief natural-language status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require local-network TV access, uv, and SONY_TV_IP, SONY_TV_PSK, and SONY_TV_MAC configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
