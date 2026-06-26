## Description: <br>
Local-first AI model routing for serious agents. One endpoint. Any provider. The router figures out the rest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Sage Router to connect coding agents and AI clients to a local or hosted OpenAI-compatible routing endpoint that selects providers by intent, latency, capability, and availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The router can handle provider credentials and may reuse local ChatGPT/OpenClaw session credentials for Codex requests. <br>
Mitigation: Use app-owned credential import where possible, avoid raw OAuth tokens in environment variables, and disable Codex OAuth routing unless it is required. <br>
Risk: The built-in dashboard and local router may expose sensitive provider configuration if reachable from untrusted networks. <br>
Mitigation: Keep the dashboard private and expose bootstrap or 0.0.0.0 listeners only on a trusted private Tailnet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/earlvanze/skills/sage-router) <br>
- [Sage Router Quickstart](https://sagerouter.dev/quickstart) <br>
- [Sage Router API Reference](https://sagerouter.dev/docs/api-reference) <br>
- [Sage Router Codex Setup](https://sagerouter.dev/docs/codex) <br>
- [Dario Anthropic Compatibility Proxy](https://github.com/askalf/dario) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown with inline shell, TOML, JSON, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service commands, endpoint URLs, environment variables, and provider configuration guidance.] <br>

## Skill Version(s): <br>
4.157.6 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
