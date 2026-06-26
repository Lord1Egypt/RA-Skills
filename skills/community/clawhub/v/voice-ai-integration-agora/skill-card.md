## Description: <br>
Helps agents guide developers through Agora real-time voice, video, chat, live streaming, recording, token generation, and voice AI integrations across web, mobile, and server platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyuguo-agora](https://clawhub.ai/user/chenyuguo-agora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, and troubleshoot Agora RTC, RTM, Conversational AI, Cloud Recording, token generation, CLI, and multi-product integration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agora CLI workflows can install tools, create or select projects, enable features, and write local environment files. <br>
Mitigation: Require confirmation before global installs, project creation or selection, feature enablement, --with-secrets exports, and .env.local writes. <br>
Risk: The skill can involve OAuth sessions, App Certificates, tokens, and other sensitive Agora credentials. <br>
Mitigation: Keep generated environment files out of source control, redact secrets from logs and shared output, and generate production tokens server-side. <br>
Risk: Recording, screen sharing, transcript, microphone, and camera flows can introduce consent, retention, and privacy obligations. <br>
Mitigation: Review these flows for user consent, data retention, and deployment-specific compliance requirements before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenyuguo-agora/voice-ai-integration-agora) <br>
- [Agora Skill Definition](artifact/SKILL.md) <br>
- [Agora Conversational AI Engine](artifact/references/conversational-ai/README.md) <br>
- [Multi-Product Integration Patterns](artifact/references/integration-patterns.md) <br>
- [Documentation Lookup](artifact/references/doc-fetching.md) <br>
- [Agora Doc MCP Server](artifact/references/mcp-tools.md) <br>
- [Agora Console](https://console.agora.io) <br>
- [Agora Docs Sitemap](https://docs.agora.io/en/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project setup steps, SDK integration guidance, token-handling instructions, and testing recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter version: 1.5.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
