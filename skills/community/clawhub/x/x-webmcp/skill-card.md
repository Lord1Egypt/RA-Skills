## Description: <br>
Connects agents to X and Grok through the local-mcp X adapter and a fixed UXC link so they can read timelines, inspect tweets, post on X, and chat with Grok from an authenticated browser profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate an authenticated X profile through local-mcp, including reading timelines and conversations, publishing tweets or articles after confirmation, and chatting with Grok. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect a live X account when directed to post, reply, publish an article, or upload files. <br>
Mitigation: Use dry-run modes where available and require user review before any non-dry-run write, publish, or upload action. <br>
Risk: Local file paths supplied for uploads or article publishing can send unintended files to X or Grok. <br>
Mitigation: Use absolute paths only for files the user intentionally selected for upload or publishing. <br>
Risk: An authenticated X profile may expose account data or actions beyond the immediate request. <br>
Mitigation: Keep the X browser profile isolated and verify authentication state before using account-dependent tools. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [X](https://x.com) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/x-webmcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON command output from x-webmcp-cli; write actions should be dry-run or explicitly reviewed before non-dry-run execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
