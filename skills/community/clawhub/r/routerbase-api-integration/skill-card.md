## Description:

Integrate applications with RouterBase, the OpenAI-compatible model gateway at https://routerbase.com/v1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenlee123](https://clawhub.ai/user/zenlee123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate or create OpenAI-compatible integrations that send requests through RouterBase, including chat completions, streaming, JSON mode, tool calling, vision inputs, and framework-specific setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or application data may be routed through RouterBase when generated examples are run.

Mitigation: Use the skill only when RouterBase routing is intended, and review what data a request sends before executing live tests.

Risk: RouterBase API keys could be exposed if copied into browser code, mobile clients, logs, or public repositories.

Mitigation: Keep ROUTERBASE_API_KEY in server-side environment configuration and use placeholders in documentation.

## Reference(s):

- [RouterBase API Reference Notes](references/routerbase-api.md)
- [RouterBase](https://routerbase.com)
- [RouterBase Documentation](https://docs.routerbase.com)
- [RouterBase Chat Completions API](https://docs.routerbase.com/api-reference/chat-completions)
- [ClawHub Skill Page](https://clawhub.ai/zenlee123/skills/routerbase-api-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run validation steps and notes to verify current model availability or pricing against the live RouterBase catalog.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
