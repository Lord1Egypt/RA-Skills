## Description: <br>
Guides an agent using ZeroToken MCP via OpenClaw for browser automation, trajectory recording, and low-token replay, especially for recurring or scheduled browser tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AMOS144](https://clawhub.ai/user/AMOS144) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to set up and operate ZeroToken browser automation through OpenClaw, record browser trajectories, convert repeatable tasks into reusable low-token scripts, and run scheduled jobs through explicit job bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ZeroToken MCP HTTP service could expose browser automation controls if bound beyond localhost. <br>
Mitigation: Keep the MCP HTTP service bound to localhost and only enable it in environments where browser automation is intended. <br>
Risk: Recorded trajectories or reusable scripts may capture secrets, account state, or sensitive inputs. <br>
Mitigation: Review trajectories and scripts before reuse, parameterize sensitive values, and avoid storing secrets directly in reusable automation. <br>
Risk: Scheduled jobs can repeatedly act on logged-in accounts and may amplify mistakes or stale task assumptions. <br>
Mitigation: Bind scheduled jobs explicitly by job_id, review default variables, and monitor session results for failed or unexpected browser actions. <br>
Risk: Tasks with many fuzzy or human-judgment steps may be unreliable when replayed unattended. <br>
Mitigation: Use reusable scripts only for stable repeatable flows and configure manual review or decision points for ambiguous steps. <br>


## Reference(s): <br>
- [ZeroToken project homepage](https://github.com/AMOS144/zerotoken) <br>
- [ClawHub skill page](https://clawhub.ai/AMOS144/zerotoken) <br>
- [Publisher profile](https://clawhub.ai/user/AMOS144) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, job ID bindings, replay variables, and operational guidance for ZeroToken MCP browser sessions.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
