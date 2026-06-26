## Description: <br>
Manage Statamic content through a tool execution gateway (composer require stokoe/ai-gateway). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michael-stokoe](https://clawhub.ai/user/michael-stokoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to discover allowed Statamic gateway tools and manage entries, globals, navigation, taxonomy, cache, and static output across configured sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway execution can change real Statamic site content when configured against production. <br>
Mitigation: Run write tests against staging or disposable content first, use allowlisted targets, and review operations before execution. <br>
Risk: The site registry contains bearer tokens for configured Statamic sites. <br>
Mitigation: Keep sites.json private, restrict file permissions, and use scoped or rotated tokens where possible. <br>
Risk: Some gateway tools may require explicit confirmation before execution. <br>
Mitigation: Show the operation summary to the user and resend with a confirmation token only after approval. <br>


## Reference(s): <br>
- [AI Gateway API Reference](references/api.md) <br>
- [Installation and Setup](INSTALL.md) <br>
- [Statamic AI Gateway Homepage](https://github.com/stokoe/ai-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON request envelopes and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured site registry, bearer tokens, curl, and jq.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
