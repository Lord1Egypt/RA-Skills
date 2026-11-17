## Description:

Use when the user needs Xcode build/test/run workflows, simulator or device control, UI automation, screenshots/video, logs, or LLDB debugging through XcodeBuildMCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ipavlidakis](https://clawhub.ai/user/ipavlidakis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run repeatable Xcode build, test, simulator, device, UI automation, logging, media capture, and debugging workflows through XcodeBuildMCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP setup examples use unpinned network package installation, which can install changing package contents over time.

Mitigation: Review the MCP setup before installation, prefer pinned package versions from a trusted source, and avoid running install commands with elevated privileges.

Risk: Device and simulator workflows can launch, install, erase, or interact with the wrong target if the target is ambiguous.

Mitigation: List available targets and confirm the exact simulator or device before launch, install, erase, clean, or similar actions.

Risk: Screenshots, recordings, logs, and debugger output can expose sensitive application or user data.

Mitigation: Use sanitized test data and review captured media, logs, and debugger output before sharing or storing them.

## Reference(s):

- [XcodeBuildMCP Setup](references/mcp-setup.md)
- [Xcodebuildmcp Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline tool names, JSON configuration examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed and configured XcodeBuildMCP server, macOS 14.5 or newer, Xcode 16.x, and Node.js 18.x or newer.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
