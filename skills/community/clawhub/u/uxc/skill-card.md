## Description: <br>
Discover and call remote schema-exposed interfaces with UXC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to discover remote schema-exposed operations, inspect their inputs, and execute OpenAPI, GraphQL, gRPC, MCP, or JSON-RPC calls through a consistent UXC CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send agent data to arbitrary external services through remote API calls. <br>
Mitigation: Use only trusted endpoints, inspect schemas before execution, and require explicit approval before calls that write data, change accounts, post publicly, or perform business or financial actions. <br>
Risk: Credential-backed API links and auth bindings may persist beyond a single task. <br>
Mitigation: Use least-privilege credentials, prefer header-based authentication where possible, and periodically review and prune persistent UXC links and auth bindings. <br>


## Reference(s): <br>
- [UXC Skill Page](https://clawhub.ai/jolestar/uxc) <br>
- [UXC Installation](https://github.com/holon-run/uxc#installation) <br>
- [Authentication Configuration Guide](references/auth-configuration.md) <br>
- [OAuth And Binding](references/oauth-and-binding.md) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Protocol Cheatsheet](references/protocol-cheatsheet.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Public Endpoints](references/public-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON envelope expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default runtime output is a machine-readable JSON envelope with ok, kind, data, error, and related metadata fields.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
