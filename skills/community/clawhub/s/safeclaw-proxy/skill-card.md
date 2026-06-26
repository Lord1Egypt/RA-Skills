## Description: <br>
Install and verify the SafeClaw safety proxy for OpenClaw and other OpenAI-compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aceteam-ai](https://clawhub.ai/user/aceteam-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install or connect to a SafeClaw proxy, route OpenClaw or OpenAI-compatible client traffic through it, and verify that calls appear in the dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reroute model traffic, edit local model-routing configuration, and start a proxy service. <br>
Mitigation: Review intended configuration changes before execution, keep backups for edited files, and verify which client path is actually routed through the proxy. <br>
Risk: API keys may be passed to a container, hosted proxy URL, or test call. <br>
Mitigation: Require explicit approval before sharing credentials, prefer trusted local endpoints, and avoid sending secrets to unverified hosted services. <br>
Risk: The skill may request elevated execution or create long-running background services. <br>
Mitigation: Approve privilege changes separately, prefer pinned image or package versions, and ask for rollback commands for every file or setting changed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup status, health-check results, routing notes, and rollback-relevant details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
