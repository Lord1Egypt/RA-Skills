## Description:

Projects a web page or Plex stream fullscreen on a second laptop over SSH and helps diagnose playback audio issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use the skill to check the remote laptop's proxy and browser state, open a page on its screen, and diagnose muted Plex playback. It is intended for explicit requests to manage that projection or its audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening a page may close unrelated browser sessions or delete Firefox recovery data; Brave may use normal browsing data instead of an isolated profile.

Mitigation: Before running the open command, check whether browser sessions or recovery data need to be preserved. Use the dedicated Firefox profile when profile isolation matters, and disclose the normal-profile behavior before choosing Brave.

Risk: The audio troubleshooting trigger may be unclear about which device its settings affect.

Mitigation: Confirm the target device and the user's intent before changing remote audio settings; report measured state and ask before raising system volume.

## Reference(s):

- [Projecting a Page Onto Another Machine](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261110-projecting-a-page-onto-another-machine.md)
- [A Skill or an MCP Server?](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261111-skill-vs-mcp.md)
- [xps-plex on ClawHub](https://clawhub.ai/j3ffyang/skills/xps-plex)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Shell commands with concise text guidance and key-value status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can report proxy, browser, window, and fullscreen state.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
