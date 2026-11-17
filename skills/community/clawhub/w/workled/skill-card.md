## Description:

workled syncs agent states (`thinking`, `waiting`, `idle`, and `error`) to a workled device over MCP and lets agents configure LED effects and touch macros.

This skill is ready for commercial/non-commercial use.

## Publisher:

[git-hub-cloud](https://clawhub.ai/user/git-hub-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use workled to connect a physical workled device to supported AI coding clients, show agent status through LEDs, and manage touch-pad macros and lighting effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent client hooks, plugins, or MCP configuration that can affect local agent behavior.

Mitigation: Install only for a reviewed client selected with `--client`, inspect the targeted client configuration, and uninstall wiring that is no longer needed.

Risk: The workled device endpoint is described as a local HTTP MCP endpoint and the security evidence flags an apparently unauthenticated device endpoint.

Mitigation: Use the skill only with trusted devices on trusted local networks, verify the configured device URL, and avoid exposing the endpoint outside the LAN.

Risk: Touch macros can type keystrokes, including password segments, through the paired device.

Mitigation: Avoid password macros unless the device transport is protected, the device is physically secure, and input focus is confirmed before triggering the macro.

Risk: Some install paths may request sudo or UAC elevation for dsh installation.

Mitigation: Approve elevation only after reviewing the selected client target and confirming that the source and device are trusted.

## Reference(s):

- [workled MCP Device Setup](references/device_setup.md)
- [Macro Format Reference](references/macro_format.md)
- [ClawHub skill page](https://clawhub.ai/git-hub-cloud/skills/workled)
- [Video demo](https://www.bilibili.com/video/BV1FK4k6WEKe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets; MCP tool calls use JSON string arguments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status diagnostics return JSON, and touch macros are configured as JSON arrays.]

## Skill Version(s):

0.1.31 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
