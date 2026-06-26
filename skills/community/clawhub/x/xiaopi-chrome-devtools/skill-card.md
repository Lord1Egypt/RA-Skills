## Description: <br>
Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-din](https://clawhub.ai/user/a-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect pages, automate browser interactions, debug web behavior, review network activity, and gather performance or visual state from Chrome DevTools through MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a mutable npm package for Chrome DevTools MCP. <br>
Mitigation: Pin the npm package version before using it in controlled or repeatable environments. <br>
Risk: The configured Chrome launch arguments disable sandbox protections. <br>
Mitigation: Remove the no-sandbox flags unless the runtime container requires them. <br>
Risk: DevTools-level browser access and persistent browser state can affect sensitive logged-in sessions. <br>
Mitigation: Use a dedicated disposable Chrome profile and avoid sensitive accounts or pages where unintended clicks, form submissions, or script execution would matter. <br>


## Reference(s): <br>
- [Chrome DevTools Documentation](https://developer.chrome.com/docs/devtools) <br>
- [Chrome DevTools AI Assistance](https://developer.chrome.com/docs/devtools/ai-assistance) <br>
- [Chrome DevTools MCP Troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide DevTools MCP browser actions against the currently selected page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
