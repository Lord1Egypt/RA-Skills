## Description:

Build sandboxed applications for secure code execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativerezz](https://clawhub.ai/user/creativerezz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Cloudflare Sandbox SDK applications for isolated code execution, AI code interpreters, CI/CD systems, and interactive development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated implementation guidance may include powerful sandbox operations such as command execution, package installation, file deletion, sandbox destruction, or preview port exposure.

Mitigation: Review command, file, lifecycle, and port operations before use; scope sandbox IDs by user or session; and confirm destructive cleanup when sandbox state should be preserved.

## Reference(s):

- [Sandbox SDK API Reference](references/api-quick-ref.md)
- [Sandbox SDK Examples](references/examples.md)
- [Cloudflare Sandbox Documentation](https://developers.cloudflare.com/sandbox/)
- [Cloudflare Sandbox API](https://developers.cloudflare.com/sandbox/api/)
- [Cloudflare Sandbox Get Started](https://developers.cloudflare.com/sandbox/get-started/)
- [Expose Services Guide](https://developers.cloudflare.com/sandbox/guides/expose-services/)
- [Cloudflare Sandbox SDK Examples](https://github.com/cloudflare/sandbox-sdk/tree/main/examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance favors retrieval from Cloudflare documentation before implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
