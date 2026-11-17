## Description:

Specialized knowledge for developing Java applications with the Solon framework, covering core concepts, web, data, security, remoting, AI, flow orchestration, cloud-native, testing, and Solon's independent annotation and plugin ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noear](https://clawhub.ai/user/noear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Solon-specific guidance, examples, and project patterns for Java application development without mixing in Spring APIs or dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security examples may include copyable insecure authentication, authorization, CORS, secret-handling, logging, or agent-permission patterns.

Mitigation: Review generated security-sensitive code before production use and require real token validation, deny-by-default authorization, trusted-origin allowlists, externally managed unique secrets, retention controls, and least-privilege tool permissions.

Risk: The skill can generate framework-specific Java code and configuration that may be unsuitable if applied outside a Solon project.

Mitigation: Confirm the target project uses Solon and review dependencies, annotations, entry points, and configuration files before applying generated changes.

## Reference(s):

- [Solon Official Website](https://solon.noear.org)
- [Solon GitHub Repository](https://github.com/opensolon/solon)
- [Quick Start](references/quick_start.md)
- [Core Concepts](references/core_concepts.md)
- [API and Annotations Reference](references/api_annotations.md)
- [Modules Reference](references/modules_reference.md)
- [Common Patterns](references/common_patterns.md)
- [Security](references/security.md)
- [Remoting](references/remoting.md)
- [AI Development](references/ai_development.md)
- [Flow Orchestration](references/flow_orchestration.md)
- [Cloud Native](references/cloud_native.md)
- [Testing](references/testing.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese responses and code comments when the user communicates in Chinese.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
