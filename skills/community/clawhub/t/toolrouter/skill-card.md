## Description:

Discover and run ToolRouter tools through one MCP connection for web research, scraping, SEO, media generation, business data, and authorized connected-account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blakefolgado](https://clawhub.ai/user/blakefolgado)

### License/Terms of Use:

MIT-0

## Use Case:

People using an assistant with ToolRouter connected can research external sources, generate media, and carry out explicitly authorized actions on connected accounts. The assistant discovers available operations and their requirements before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected-account actions could post, delete, or send messages without the intended authority.

Mitigation: Confirm the specific connected account and authorization for each action before execution.

Risk: Paid operations, including media generation, may consume credits.

Mitigation: Review operation prices and available credits and obtain spending approval before use.

Risk: Remote tool access may involve sensitive provider credentials and account permissions.

Mitigation: Review provider permissions and keep credentials in the client credential store, not chat or shared configuration.

## Reference(s):

- [ToolRouter homepage](https://toolrouter.com)
- [ToolRouter setup guide](https://toolrouter.com/docs/markdown/quickstart)
- [Provider reference](references/providers.md)
- [Provider index](https://toolrouter.com/providers.md)
- [Tool catalog](https://api.toolrouter.com/v1/tools)
- [ToolRouter API schema](https://api.toolrouter.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with source or completed-asset links and verified action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and available actions depend on the live catalog, connected accounts, and credits.]

## Skill Version(s):

1.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
