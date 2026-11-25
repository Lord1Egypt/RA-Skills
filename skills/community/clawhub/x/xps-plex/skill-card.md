## Description:

Projects a requested web page onto a second laptop over SSH and helps diagnose proxy, browser, fullscreen, and page audio status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a configured second laptop use this skill to project pages or streams, check proxy and browser state, and diagnose muted playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening a page can close unrelated browser windows or remove Firefox session recovery data.

Mitigation: Use the open action only for an explicit page request, and check the current browser windows before proceeding when they may contain unrelated work.

Risk: Reusing a browser window may not reliably open the requested page.

Mitigation: Confirm the reported window title and fullscreen state before reporting that the page opened.

Risk: A mute shortcut can reach the wrong window or fail to unmute the page.

Mitigation: Focus the intended page by its window address and verify an active browser audio stream before reporting that playback is unmuted.

## Reference(s):

- [xps-plex on ClawHub](https://clawhub.ai/j3ffyang/skills/xps-plex)
- [Projecting a Page Onto Another Machine](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261110-projecting-a-page-onto-another-machine.md)
- [A Skill or an MCP Server?](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261111-skill-vs-mcp.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Shell commands and concise status or diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports proxy, browser, and window state; may start the proxy or browser and open the configured page.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
