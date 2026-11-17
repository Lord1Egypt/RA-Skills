## Description:

Create fallback site adapters for websites that do not expose native WebMCP. Use when a site needs a new adapter module, tool schema design, browser-side request execution, or request-template extraction from observed page behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or update fallback SiteAdapter modules for websites that do not expose native WebMCP. It guides adapter scaffolding, browser-side request discovery, stable tool-contract design, fallback behavior, and testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold helper has a confirmed command-execution flaw when crafted host, URL, display name, or package name values are supplied.

Mitigation: Review and fix the Perl replacement handling before running the helper with untrusted values; until then, only run it with trusted inputs and minimal secrets in the environment.

Risk: Generated adapters can act through a logged-in browser session.

Mitigation: Keep adapter behavior scoped to explicit user intent, avoid credential replay or secret vaulting, and fail closed on authentication, challenge, or upstream-change states.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/webmcp-adapter-creator)
- [Workflow](artifact/references/workflow.md)
- [Network Discovery](artifact/references/network-discovery.md)
- [Request Template Patterns](artifact/references/request-template-patterns.md)
- [Adapter Runtime Patterns](artifact/references/adapter-runtime-patterns.md)
- [Testing](artifact/references/testing.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated adapter source/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated adapters should keep privileged site actions in the browser page context and return JSON-serializable tool payloads.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
