## Description:

Ubuntu Ollama helps agents guide Ubuntu users through setting up Ollama fleet routing across multiple machines with apt, systemd, CUDA, health checks, and API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Ubuntu machines as an Ollama fleet with a router, worker nodes, systemd services, CUDA acceleration, monitoring endpoints, and OpenAI-compatible or Ollama-compatible request examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to create persistent root-managed systemd services.

Mitigation: Review service definitions before enabling them, create a dedicated non-root service account where possible, and keep disable or rollback commands available.

Risk: The skill opens Ollama fleet routing on port 11435.

Mitigation: Restrict port 11435 to trusted hosts or a VPN instead of exposing it broadly.

Risk: The skill includes a curl-to-shell installation command and package installation steps.

Mitigation: Review installation scripts before execution and pin or verify packages where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ubuntu-ollama)
- [Ollama Herd GitHub project](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash, Python, systemd, and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Ubuntu-specific prerequisites, optional tool requirements, service configuration, firewall guidance, monitoring commands, and guardrails for model download and deletion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
