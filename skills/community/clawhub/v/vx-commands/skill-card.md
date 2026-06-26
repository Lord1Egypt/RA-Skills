## Description: <br>
Complete vx CLI command reference for looking up command syntax, flags, output formats, token-efficient forwarding, and vx-native structured output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to look up vx CLI commands, structured output modes, forwarding behavior, global flags, and practical command examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some documented commands can print environment details or use authenticated tools, which may expose secrets or local development state. <br>
Mitigation: Review command output before sharing it, avoid forwarding full environment output, and pay special attention to authenticated CLI usage. <br>
Risk: Some documented commands install or remove tools, clean caches, export shell variables, or modify vx.toml and vx.lock. <br>
Mitigation: Approve state-changing commands only for the intended project and inspect proposed changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/vx-commands) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-reference guidance only; no executable payload is bundled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
