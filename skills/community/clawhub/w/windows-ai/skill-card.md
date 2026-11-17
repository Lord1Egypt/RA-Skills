## Description:

Windows AI helps agents guide users through running local AI workloads on Windows PCs with LLM inference, image generation, embeddings, and multi-PC Ollama Herd routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows AI operators use this skill to install, configure, and use a local OpenAI-compatible AI endpoint backed by Ollama Herd across one or more Windows PCs. It covers local chat, coding, image generation, embeddings, dashboard access, GPU-aware routing, and basic operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned code can introduce unexpected or compromised dependencies.

Mitigation: Install in a dedicated environment and verify the `ollama-herd` package or source before installation.

Risk: Opening inbound port 11435 broadly can expose a local AI service to untrusted hosts.

Mitigation: Avoid the broad firewall command as written; restrict access to trusted private IPs or a private network profile and confirm appropriate authentication before exposing the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/windows-ai)
- [Ollama Herd project homepage](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may propose local installation, firewall, environment-variable, API-client, and model-operation steps for Windows systems.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
