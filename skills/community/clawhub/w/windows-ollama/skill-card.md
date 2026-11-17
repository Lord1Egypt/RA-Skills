## Description:

Windows Ollama helps agents set up and use Ollama Herd to route local Ollama inference across multiple Windows PCs, with load balancing, health checks, dashboard monitoring, and NVIDIA RTX GPU-aware examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a Windows Ollama Herd fleet, route OpenAI- or Ollama-compatible requests across Windows PCs, and monitor router and node health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening the router port broadly can expose the local AI service outside trusted hosts.

Mitigation: Restrict port 11435 to trusted private networks or specific IP addresses before enabling the firewall rule.

Risk: Installing and running the Python package and local services with elevated privileges can increase operational risk.

Mitigation: Use a non-admin virtual environment where possible and pin or review the package version before installation.

Risk: Model downloads and deletions can affect local storage, bandwidth, and service availability.

Mitigation: Keep explicit user confirmation for model downloads and deletion, and do not automate model pulls without opt-in.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/windows-ollama)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama](https://ollama.ai)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell, Python, curl, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows-specific commands, local service URLs, model recommendations, and guardrails for model downloads and deletion.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
