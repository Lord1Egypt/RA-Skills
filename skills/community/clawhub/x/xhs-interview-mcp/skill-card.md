## Description:

Helps agents use a local Xiaohongshu MCP service to search interview-experience posts, fetch note details, view recommendations, and check account status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisdontknowcoding](https://clawhub.ai/user/krisdontknowcoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Xiaohongshu interview-experience content through a local MCP service and extract useful note details for hiring or career research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local MCP service uses downloaded external binaries that handle Xiaohongshu session data.

Mitigation: Verify the binary source and integrity independently before use, and run the service without elevated privileges.

Risk: The service stores account cookies locally and runs as a background process.

Mitigation: Use it only on trusted machines, protect or remove cookies when finished, and stop the background service after the task.

Risk: The available tools can like, favorite, or comment from the user's account.

Mitigation: Keep workflows read-only by default and require explicit user confirmation before account-modifying actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krisdontknowcoding/skills/xhs-interview-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local MCP service responses including Xiaohongshu note metadata, comments, images, and account status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
