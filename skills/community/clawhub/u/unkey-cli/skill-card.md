## Description: <br>
Unkey CLI helps agents manage Unkey API namespaces, keys, identities, permissions, rate limits, analytics queries, and related troubleshooting from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer Unkey resources with the official CLI, including API namespaces, API keys, RBAC permissions, identities, rate limits, and verification analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill helps administer sensitive Unkey API keys, permissions, namespaces, and rate limits. <br>
Mitigation: Use the least-privileged Unkey credential available, do not paste full root keys into chat, and review commands that create, delete, or change keys, permissions, namespaces, or rate limits. <br>
Risk: The skill may suggest installing or invoking the Unkey CLI from the local environment. <br>
Mitigation: Verify the Unkey CLI package source before installation or execution. <br>
Risk: Delete or update operations can make irreversible or disruptive changes to Unkey resources. <br>
Mitigation: Confirm authentication source and require explicit user confirmation before executing destructive or modifying commands. <br>


## Reference(s): <br>
- [Unkey documentation index](https://unkey.com/docs/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/unkey-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should avoid exposing full root keys and should use JSON output for scripting when appropriate.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
