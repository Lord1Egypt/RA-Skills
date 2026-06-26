## Description: <br>
Use when the user needs Xcode build/test/run workflows, simulator or device control, UI automation, screenshots/video, logs, or LLDB debugging through XcodeBuildMCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipavlidakis](https://clawhub.ai/user/ipavlidakis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to guide XcodeBuildMCP-based build, run, test, simulator/device control, UI automation, logging, screenshot/video, and LLDB debugging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful Xcode automation, including simulator and device actions, screenshots, logs, video recording, physical-device installs, and LLDB commands. <br>
Mitigation: Use test projects or devices when possible, review proposed actions before execution, and require explicit confirmation for sensitive or destructive workflows. <br>
Risk: The setup guidance includes installing the external XcodeBuildMCP package with a moving latest version. <br>
Mitigation: Prefer pinning and reviewing the external package version before allowing an agent to use the MCP server. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ipavlidakis/xcodebuildmcp) <br>
- [XcodeBuildMCP setup](references/mcp-setup.md) <br>
- [Xcodebuildmcp workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline MCP tool names and shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on a configured XcodeBuildMCP server, Xcode, and available simulator or device targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
