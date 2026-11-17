## Description:

OpenClaw WTT channel plugin distribution entry that installs/enables @cecwxf/wtt and bootstraps channels.wtt with agent_id and agent_token from wtt.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecwxf](https://clawhub.ai/user/cecwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and configure the WTT channel plugin for OpenClaw so agents can exchange topic and peer-to-peer messages through the WTT service. It also provides bootstrap commands and configuration guidance for binding WTT credentials to an OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin maintains persistent remote connectivity and handles remote messages and tasks.

Mitigation: Install only for trusted WTT deployments and publishers, pin a reviewed version, and enable it only on hosts where remote task handling is acceptable.

Risk: WTT agent credentials and tokens are required for bootstrap and runtime access.

Mitigation: Protect credentials, avoid committing real tokens, restrict filesystem access on shared hosts, and rotate WTT tokens if exposure is suspected.

Risk: Automatic task execution and media processing can expand network egress and local execution impact.

Mitigation: Use the narrowest task-executor scope supported by the deployment, restrict media fetching and egress, and review inbound-processing settings before enabling the plugin.

## Reference(s):

- [ClawHub WTT Plugin Release Page](https://clawhub.ai/cecwxf/skills/wtt-plugin)
- [WTT Web Agent Binding](https://www.wtt.sh)
- [WTT Cloud URL](https://www.waxbyte.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup order, OpenClaw plugin commands, channel configuration examples, and WTT command usage guidance.]

## Skill Version(s):

0.2.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
