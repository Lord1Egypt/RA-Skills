## Description: <br>
Local-first AI model routing for serious agents. One endpoint. Any provider. The router figures out the rest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Sage Router to expose one OpenAI- or Anthropic-compatible endpoint that routes agent requests across local, self-hosted, and authorized external model providers. It helps coding agents and AI tools choose models by intent, capability, latency, and fallback health while preserving a local-first credential custody posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server can expose routing and setup controls if port 8790 is reachable without authentication. <br>
Mitigation: Bind it to localhost or place it behind a secured reverse proxy, and set SAGE_ROUTER_CLIENT_API_KEYS or SAGE_ROUTER_CLIENT_AUTH_REQUIRED=1 before exposing it to a network. <br>
Risk: Provider credentials may be available to the router process through environment variables or mounted credential files. <br>
Mitigation: Run only on a trusted machine or network, and mount only the provider credential directories the router is intended to use. <br>
Risk: Self-hosted and hosted modes have different authentication, billing, analytics, and persistence behavior. <br>
Mitigation: Review the Security & Privacy documentation and enable hosted Supabase, billing, analytics, or public edge features only when their operational controls are configured. <br>


## Reference(s): <br>
- [Sage Router on ClawHub](https://clawhub.ai/earlvanze/skills/sage-router) <br>
- [README](README.md) <br>
- [Security & Privacy](SECURITY.md) <br>
- [Sage Router architecture](docs/architecture.md) <br>
- [Sage Router Integration Guides](docs/integrations/README.md) <br>
- [Use Sage Router with NVIDIA NIM / NVIDIA Cloud](docs/integrations/nvidia-nim.md) <br>
- [Use Sage Router as an OpenAI-compatible endpoint](docs/integrations/openai-compatible.md) <br>
- [Use Sage Router with Codex CLI](docs/integrations/codex.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, JSON snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and routing guidance for agent tools; it may reference local files, environment variables, endpoints, and provider configuration.] <br>

## Skill Version(s): <br>
4.157.9 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
