## Description:

Manages V2Ray proxy start/stop behavior and system proxy configuration based on network connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:

MIT License

## Use Case:

Developers and operators use this skill to manage a local V2Ray/Xray proxy, switch proxy state automatically when selected network checks fail, and inspect proxy status from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent shell profile changes can affect future sessions without enough user visibility.

Mitigation: Review the skill before installing and remove or make opt-in any writes to ~/.bashrc.

Risk: Proxy changes and background V2Ray/Xray processes can affect local networking beyond the immediate command.

Mitigation: Document the networking impact clearly, verify proxy state with status commands, and ensure proxy cleanup runs after use.

Risk: Eval-based command wrapping and broad process matching can execute arguments unsafely or stop unrelated processes.

Mitigation: Replace eval-based wrapping with direct argument execution and manage only a recorded V2Ray/Xray process ID.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bombfuock/skills/vpn-proxy-manager)
- [Publisher Profile](https://clawhub.ai/user/bombfuock)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local networking commands and status output for a V2Ray/Xray proxy setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
