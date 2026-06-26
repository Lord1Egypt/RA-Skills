## Description: <br>
Scalekit Agent Auth helps OpenClaw agents discover, authorize, and execute actions against connected third-party services through Scalekit Connect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avinash-kamath](https://clawhub.ai/user/avinash-kamath) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to external SaaS tools, discover available provider actions, authorize accounts, execute tool calls, and fall back to proxied API requests when a catalog tool is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act across connected third-party services using configured Scalekit credentials. <br>
Mitigation: Use least-privilege Scalekit credentials, connect only required providers, and require explicit approval before mutating actions. <br>
Risk: The authorization inspection command can print raw OAuth tokens. <br>
Mitigation: Do not use --get-authorization in agent workflows and avoid logging command output. <br>
Risk: Proxy requests and file transfers may bypass curated tool schemas and can send, delete, upload, or download data. <br>
Mitigation: Require explicit approval before proxy requests, file transfers, sends, deletes, or other mutating actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avinash-kamath/scalekit-agent-auth) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Scalekit Connect](https://scalekit.com) <br>
- [Scalekit Notion connector setup guide](https://docs.scalekit.com/reference/agent-connectors/notion/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return provider data, authorization links, tool schemas, execution results, or setup guidance depending on the requested connected service action.] <br>

## Skill Version(s): <br>
2.4.2 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
