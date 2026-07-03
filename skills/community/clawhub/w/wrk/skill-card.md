## Description: <br>
Use wrk for HTTP load testing, including Lua scripting for dynamic request headers such as randomized X-Forwarded-For IPs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix-montanari](https://clawhub.ai/user/felix-montanari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, run, and interpret authorized HTTP load tests with wrk, including Lua-based request generation for dynamic headers and request bodies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Load tests can disrupt services or third-party systems if run without authorization or at high volume. <br>
Mitigation: Confirm authorization, prefer local, development, staging, sandbox, or approved performance-test environments, and start with low traffic before scaling while monitoring service health and dependencies. <br>
Risk: Randomized X-Forwarded-For examples can affect logging, rate limits, WAF behavior, cache behavior, and audit trails. <br>
Mitigation: Use randomized IP headers only when the target team has explicitly approved that scenario and understands the operational and audit impacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felix-montanari/skills/wrk) <br>
- [wrk GitHub repository](https://github.com/wg/wrk) <br>
- [Publisher profile](https://clawhub.ai/user/felix-montanari) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with shell and Lua code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes authorization checks, conservative starting parameters, and interpretation checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
