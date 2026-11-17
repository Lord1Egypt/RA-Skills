## Description:

Builds an AI e-commerce customer service web app with TRTC Conversational AI, real-time voice and text modes, Chinese, English, and Cantonese support, order workflows, shipping tracking, returns, promotions, and optional digital avatar support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryang-cool](https://clawhub.ai/user/jerryang-cool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold or integrate a TRTC Conversational AI e-commerce customer service web app with voice, text, multilingual UI, order workflows, and optional digital avatar support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated app exposes unauthenticated cloud-control and credential-issuing endpoints.

Mitigation: Add authentication, rate limits, and room or task ownership checks before customer-facing deployment.

Risk: The generated configuration uses cloud API keys, TRTC secrets, and LLM keys that can affect billing and access if exposed.

Mitigation: Protect env.yaml, use least-privilege cloud credentials, and move production secrets into an approved secret-management system.

Risk: The startup flow can offer to kill the process listening on port 8080.

Mitigation: Inspect the displayed PID and command before approving termination, and decline when the process is unknown.

Risk: External SDKs and package dependencies may change over time.

Mitigation: Pin or self-host SDK assets and review dependency versions before deployment.

Risk: LLM configuration and user conversation content may be routed through TRTC cloud services and the configured LLM provider.

Mitigation: Review provider data handling policies and apply data minimization or redaction for sensitive customer information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryang-cool/skills/trtc-ai-customer-service)
- [Architecture reference](artifact/references/architecture.md)
- [Configuration guide](artifact/references/config-guide.md)
- [Frontend integration guide](artifact/references/frontend-guide.md)
- [Tencent RTC console](https://console.trtc.io/)
- [TRTC Conversational AI solution](https://trtc.io/solutions/conversational-ai)
- [TRTC LLM configuration guide](https://trtc.io/document/68338?product=conversationalai)
- [TRTC TTS voice configuration](https://trtc.io/document/79682?product=conversationalai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code snippets and shell commands, plus generated project files when scaffolding.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a Python Flask and vanilla JavaScript TRTC customer-service app, configuration templates, startup scripts, and integration guidance.]

## Skill Version(s):

1.2.5 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
