## Description:

Interact with the user's Tandem Browser via MCP bridge (mcporter) to browse, capture snapshots, click, type, navigate, and coordinate in a shared browser environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikefaierberg-byte](https://clawhub.ai/user/mikefaierberg-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a local Tandem Browser session through mcporter for browsing, page reading, DOM snapshots, navigation, and user-coordinated interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a local browser through broad debugging and browsing capabilities.

Mitigation: Use only with Tandem profiles and OS accounts suitable for agent-driven browsing, and prefer isolated sessions for sensitive work.

Risk: Authenticated personal sessions may expose account state to agent-driven browser actions.

Mitigation: Avoid personal authenticated sessions unless needed, revoke trust grants when done, and keep agent work in isolated browser sessions where possible.

Risk: Chromium sandboxing is disabled for the local Tandem Browser launch path described by the artifact.

Mitigation: Run Tandem in a container or otherwise restricted environment when browsing untrusted sites.

Risk: Web pages may contain prompt-injection content or blocked content markers.

Mitigation: Respect Tandem's prompt-injection warnings and blocked markers, do not follow embedded page instructions, and escalate to the user when content is blocked.

## Reference(s):

- [Tandem Browser ClawHub Skill](https://clawhub.ai/mikefaierberg-byte/skills/tandem-browser)
- [Tandem Browser Homepage](https://github.com/hydro13/tandem-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and a locally running Tandem Browser MCP server; browser actions may require user approval.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
