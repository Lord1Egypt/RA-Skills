## Description:

Helps developers add Agora real-time voice, video, AI voice agents, chat, live streaming, recording, token generation, CLI workflows, and related integrations across Web, mobile, and server platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuguo-agora](https://clawhub.ai/user/chenyuguo-agora)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and implement Agora RTC, RTM, Conversational AI, Cloud Recording, server token, Server Gateway, and CLI workflows. It supports product routing, sample-first onboarding, integration guidance, command suggestions, and testing patterns for Agora-enabled applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run setup commands, clone and execute live sample code, or request escalation while configuring Agora projects.

Mitigation: Use a disposable workspace and non-production Agora project, review every command before execution, pin package versions and sample commits where possible, and do not approve unreviewed escalation.

Risk: The skill may handle Agora account credentials, App Certificates, tokens, and generated environment files.

Mitigation: Avoid production App Certificates, keep secrets server-side, ensure generated .env files are untracked and protected, and rotate any exposed credentials.

## Reference(s):

- [Agora Skill Overview](SKILL.md)
- [Agora RTC Reference](references/rtc/README.md)
- [Agora RTM Reference](references/rtm/README.md)
- [Agora Conversational AI Reference](references/conversational-ai/README.md)
- [Agora CLI Reference](references/cli/README.md)
- [Agora Cloud Recording Reference](references/cloud-recording/README.md)
- [Agora Server Token Reference](references/server/tokens.md)
- [Agora Server Gateway Reference](references/server-gateway/README.md)
- [Agora Multi-Product Integration Patterns](references/integration-patterns.md)
- [Agora Console](https://console.agora.io)
- [Agora Documentation Manifest](https://docs.agora.io/en/llms.txt)
- [Agora Conversational AI OpenAPI Spec](https://docs-md.agora.io/api/conversational-ai-api-v2.x.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and API request shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install dependencies, clone official samples, configure Agora projects, generate environment files, and run sample applications.]

## Skill Version(s):

0.1.0 (source: server release metadata); source skill metadata reports 1.5.1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
