## Description: <br>
Secure Python Code Sandbox executes arbitrary Python code in an isolated sandbox with pre-installed libraries including requests, NumPy, and pandas, returning stdout, stderr, and execution results through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to invoke AgentPMT's remote Python sandbox for quick computations, data manipulation, dynamic API calls, and self-contained scripting without provisioning local execution infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute arbitrary Python code and make network requests through a remote sandbox. <br>
Mitigation: Review code before invocation, constrain inputs to the minimum needed, and avoid executing attacker-supplied code unless it has been independently reviewed. <br>
Risk: Secrets, wallet material, payment headers, proprietary data, or other sensitive credentials could be exposed if included in sandbox inputs or logs. <br>
Mitigation: Do not send secrets or proprietary data to the tool; use AgentPMT setup skills and platform controls for credential handling. <br>
Risk: Long-running or oversized code can fail or consume unnecessary remote execution resources. <br>
Mitigation: Keep code self-contained, respect the documented 50,000 character input limit, and set timeout_seconds within the documented 10 to 60 second range. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/secure-python-code-sandbox) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/secure-python-code-sandbox) <br>
- [Secure Python Code Sandbox Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and Python code strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines an invoke action with required code and optional timeout_seconds parameters; remote tool responses are returned as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
