## Description:

Super Clawcompany coordinates PM, Developer, and Review agents to analyze software requests, generate code, and review implementation work for application and feature development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molexazwo](https://clawhub.ai/user/molexazwo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate a development workflow from request analysis through code generation and review. It is intended for rapid prototyping, feature implementation, and end-to-end app creation in a target project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spawn external agents that modify files in the target project.

Mitigation: Run with --dry-run first, use a disposable or version-controlled project path, and review all generated diffs before keeping changes.

Risk: The workflow depends on GLM_API_KEY and may expose sensitive configuration through verbose logs or shell history.

Mitigation: Set credentials through the environment, avoid echoing GLM_API_KEY, and do not use verbose logging with real credentials.

Risk: The built-in review gate can approve failures or accept malformed review output.

Mitigation: Perform a manual code review and run project tests before using generated code in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/molexazwo/skills/super-clawcompany)
- [Publisher Profile](https://clawhub.ai/user/molexazwo)
- [GLM API Key Portal](https://open.bigmodel.cn/)
- [Z.ai Chat Completions API](https://api.z.ai/api/coding/paas/v4/chat/completions)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and JSON summaries with generated or modified project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May spawn external coding agents and write files under the configured project path.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
