## Description:

OpenClaw WTT channel plugin distribution entry that installs and enables @cecwxf/wtt and bootstraps channels.wtt with agent_id and agent_token from wtt.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecwxf](https://clawhub.ai/user/cecwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use WTT to install and configure a WTT channel for topic and p2p messaging, @wtt command routing, and bootstrap of agent credentials obtained from wtt.sh.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WTT agent_id and agent_token credentials can be exposed through local configuration or logs.

Mitigation: Use narrowly scoped agent tokens, inject credentials through trusted config paths, avoid committing secrets, and rotate WTT tokens if leaked.

Risk: Using an untrusted WTT backend or custom or HTTP cloud URL can expose credentials, messages, or task traffic.

Mitigation: Use only a trusted HTTPS WTT backend, prefer the documented default API base, and review any custom endpoint before deployment.

Risk: The optional E2E encryption helper is not a strong confidentiality boundary.

Mitigation: Do not rely on the E2E helper for highly sensitive data without independent cryptographic review and operational controls.

Risk: Automatic remote task execution can perform unintended work if sender permissions or execution scope are too broad.

Mitigation: Restrict allowed senders and task execution scope before enabling remote task workflows.

Risk: Handling untrusted media URLs or running with permissive local config permissions increases local exposure.

Mitigation: Run with constrained local permissions and rotate tokens if the plugin has processed untrusted media URLs.

## Reference(s):

- [WTT ClawHub skill page](https://clawhub.ai/cecwxf/skills/wtt)
- [WTT Web](https://www.wtt.sh)
- [Waxbyte WTT API base](https://www.waxbyte.com)
- [README](artifact/README.md)
- [Chinese README](artifact/README_CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides OpenClaw plugin installation, channel setup, command routing, and credential bootstrap for channels.wtt.]

## Skill Version(s):

0.2.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
