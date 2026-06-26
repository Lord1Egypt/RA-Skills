## Description: <br>
Use Tabbit with agent-browser by reading Tabbit's live DevToolsActivePort file, deriving the browser wsEndpoint, and routing browser actions through agent-browser --cdp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carri1sun](https://clawhub.ai/user/carri1sun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect browser automation workflows to a user's active Tabbit browser session. It discovers Tabbit's Chromium DevTools endpoint and routes page operations through agent-browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can allow an agent to inspect and interact with pages in the user's active Tabbit browser session. <br>
Mitigation: Install and use it only when browser-session inspection and interaction are intended, and review browser actions before execution. <br>
Risk: The wrapper can launch agent-browser through a configured command or npx fallback. <br>
Mitigation: Prefer installing agent-browser yourself and avoid setting AGENT_BROWSER_BIN to untrusted commands. <br>
Risk: A custom DevToolsActivePort path can redirect discovery to an unintended browser endpoint. <br>
Mitigation: Set TABBIT_DEVTOOLS_ACTIVE_PORT_FILE only to trusted local Tabbit DevToolsActivePort files. <br>


## Reference(s): <br>
- [Tabbit Endpoint Discovery](references/discovery.md) <br>
- [Tabbit Devtools Setup](references/setup.md) <br>
- [Endpoint discovery helper](scripts/discover_tabbit_cdp.py) <br>
- [agent-browser wrapper](scripts/run_agent_browser_on_tabbit.py) <br>
- [agent-browser upstream docs](https://github.com/vercel-labs/agent-browser) <br>
- [ClawHub skill page](https://clawhub.ai/carri1sun/tabbit-devtools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style connection facts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report activePortFile, port, browserPath, browserUrl, and wsEndpoint for the active Tabbit session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
