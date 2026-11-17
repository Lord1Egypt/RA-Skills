## Description:

skill-to-http exposes installed agent Skills as HTTP(S) REST API services through a persistent FastAPI server that auto-generates endpoints, supports sync/async execution with webhook callbacks, and includes a bilingual web management console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose locally installed agent Skills as REST endpoints for internal tools, remote callers, and external systems. It helps configure and operate skill execution, async jobs, webhook callbacks, TLS, API key authentication, and management-console workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service can expose locally installed Skills as remotely callable HTTP endpoints, widening access to file, shell, network, credential, or other host capabilities available to those Skills.

Mitigation: Bind the service and console to 127.0.0.1 unless network access is required, set a strong API key, enable HTTPS for cross-host use, replace wildcard exposure with an explicit allowlist, and deny side-effecting Skills.

Risk: Default HTTP transport can send API keys, prompts, and Skill outputs in cleartext.

Mitigation: Use localhost or trusted networks only for HTTP, and enable HTTPS before cross-host or production use.

Risk: Wildcard exposure and fully automated executor paths can give untrusted callers broad ability to trigger powerful local actions.

Mitigation: Avoid wildcard exposure for shared environments, deny high-impact Skills, require confirmation in high-risk Skill frontmatter, and avoid the full-auto Codex path for untrusted callers.

Risk: A remotely reachable unauthenticated management console, speed mode, or doctor fix path can change service state or configuration.

Mitigation: Require authentication, keep management surfaces local when possible, and do not enable speed mode or doctor fixes through a remotely reachable unauthenticated console.

Risk: The optional LLM fallback and parameter extraction path can send SKILL.md content to an external chat-completions endpoint when configured.

Mitigation: Leave the LLM path off unless needed, use only trusted endpoints, and keep exposed SKILL.md files free of secrets, internal addresses, or sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/skill-to-http)
- [HTTPS Deployment Guide](references/https-deployment.md)
- [params.json Schema Reference](references/params-schema.md)
- [HTTP Skill TLS and Auth Standard](references/tls-auth-standard.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent service behavior depends on local configuration, exposed skill allowlists, executor availability, and TLS/API key settings.]

## Skill Version(s):

1.0.2 (source: server release metadata and CHANGELOG, released 2026-07-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
