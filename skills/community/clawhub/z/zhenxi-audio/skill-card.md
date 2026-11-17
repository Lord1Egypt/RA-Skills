## Description:

An assistant for connecting to the Zhenxi audio service and finding, previewing, and downloading audiobooks, storytelling recordings, and radio dramas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaokingsoft](https://clawhub.ai/user/miaokingsoft)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to connect to the Zhenxi catalog, search for titles, listen to a first-episode preview, and retrieve a complete-book download when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding an email address to the donation link shares it with a separate site.

Mitigation: Use the donation link without the email parameter unless the user explicitly agrees to share their address.

Risk: The service access token could be exposed if repeated in conversation or stored carelessly.

Mitigation: Keep the token in the MCP authorization header, protect the configuration, and never repeat the full token in chat.

Risk: Purchases use non-refundable credits and may have changing prices or limits.

Mitigation: Check current costs and limits with the service tools before purchase, and explain the applicable credit cost first.

## Reference(s):

- [Server-resolved source repository](https://github.com/miaokingsoft/zhenxi-audio/tree/main/zhenxi-audio)
- [Zhenxi audio service MCP endpoint](https://zhenxi.miaoking.com/mcp.php)
- [Audio preview player template](https://zhenxi.miaoking.com/skill/zhenxi-audio/player-template.html)
- [ClawHub skill page](https://clawhub.ai/miaokingsoft/skills/zhenxi-audio)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API calls, HTML files]

**Output Format:** [Concise text guidance, MCP configuration snippets, and HTML playback pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Playback pages use the supplied HTML template and service-returned preview details.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
