## Description:

Use Tabbit with agent-browser by reading Tabbit's live DevToolsActivePort file, deriving the browser wsEndpoint, and routing browser actions through agent-browser --cdp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carri1sun](https://clawhub.ai/user/carri1sun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect browser automation to an active local Tabbit browser session by discovering its DevTools WebSocket endpoint and passing it to agent-browser. It is intended for Tabbit-specific browser inspection and interaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-privilege browser control over a local Tabbit session.

Mitigation: Install only for trusted local Tabbit sessions, keep DevTools debugging limited to localhost, and disable Tabbit remote debugging when finished.

Risk: The wrapper can automatically run an unpinned npm package when agent-browser is not already installed.

Mitigation: Prefer a preinstalled, trusted, pinned agent-browser binary and set AGENT_BROWSER_BIN when needed.

## Reference(s):

- [Tabbit Devtools Setup](references/setup.md)
- [Tabbit Endpoint Discovery](references/discovery.md)
- [agent-browser upstream docs](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/carri1sun/skills/tabbit-devtools)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline shell commands and structured connection facts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tabbit connection fields such as activePortFile, port, browserPath, browserUrl, and wsEndpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
