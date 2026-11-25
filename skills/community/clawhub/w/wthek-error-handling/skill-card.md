## Description:

Use this skill whenever adding, refactoring, configuring, or standardizing HTTP error handling, validation error pipelines (Zod, Valibot, TypeBox), HTTP status code usage, or MCP error formatting in Express, Fastify, Hono, Koa, NestJS, Restify, Node.js applications, or Model Context Protocol servers using @wthek packages, http-error-kit, and http-response-status-code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillnter](https://clawhub.ai/user/skillnter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to choose and configure HTTP error-handling middleware, validation error transformers, and status-code utilities for their Node.js framework. It also provides patterns for formatting errors in MCP servers and for checking the resulting error-handling setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, and some referenced content was only partly inspected.

Mitigation: Review the relevant framework reference before applying its guidance, and test the resulting error responses in the target application.

Risk: The MCP setup example can prompt npx to install a package if it is not already installed.

Mitigation: Install the package explicitly first or review the npx confirmation prompt; avoid automatic yes flags.

## Reference(s):

- [Server-resolved source repository](https://github.com/Skillnter/wthek-error-handling/tree/main/skills/wthek-error-handling)
- [http-error-kit package](https://www.npmjs.com/package/http-error-kit)
- [http-response-status-code package](https://www.npmjs.com/package/http-response-status-code)
- [Express guide](artifact/references/express.md)
- [Fastify guide](artifact/references/fastify.md)
- [Hono guide](artifact/references/hono.md)
- [Koa guide](artifact/references/koa.md)
- [NestJS guide](artifact/references/nestjs.md)
- [Restify guide](artifact/references/restify.md)
- [Zod integration guide](artifact/references/zod.md)
- [Valibot integration guide](artifact/references/valibot.md)
- [TypeBox integration guide](artifact/references/typebox.md)
- [Status-code usage guide](artifact/references/status-codes.md)
- [Formatter and RFC 9457 guide](artifact/references/formatters.md)
- [MCP integration guide](artifact/references/mcp.md)
- [MCP error formatter package](https://www.npmjs.com/package/@wthek/mcp-error-formatter)
- [MCP server package](https://www.npmjs.com/package/@wthek/mcp)
- [RFC 9457 Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc9457)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown with code snippets, tables, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the project's framework and validation library; examples are provided for the listed integrations.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
