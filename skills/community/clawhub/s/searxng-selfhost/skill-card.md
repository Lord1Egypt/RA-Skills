## Description: <br>
Self-hosted web search aggregator for OpenClaw agents that installs or uses a local SearXNG instance and provides a search CLI with Wikipedia and GitHub fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saikatkumardey](https://clawhub.ai/user/saikatkumardey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to self-host web search for OpenClaw agents, configure the local SearXNG service, and run agent-readable searches without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation workflow makes system-level changes and enables a persistent local SearXNG service. <br>
Mitigation: Run the installer only on a server or VM intended for this service, and review the shell script before execution. <br>
Risk: Search queries may reach upstream search providers through SearXNG or the Wikipedia and GitHub fallback. <br>
Mitigation: Avoid sensitive search queries unless that exposure is acceptable for the deployment. <br>


## Reference(s): <br>
- [SearXNG Search Usage Reference](references/usage.md) <br>
- [SearXNG project](https://github.com/searxng/searxng) <br>
- [ClawHub skill page](https://clawhub.ai/saikatkumardey/searxng-selfhost) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, URL, snippet, and engine when emitted by the CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
