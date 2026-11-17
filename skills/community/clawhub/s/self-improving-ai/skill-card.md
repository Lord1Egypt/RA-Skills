## Description:

Captures learnings about GenAI/LLM configuration, model selection, inference optimization, fine-tuning, RAG pipelines, prompt engineering, multimodal processing, and cost management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI engineers use this skill to capture model behavior, inference, RAG, prompt, fine-tuning, multimodal, evaluation, and guardrail learnings in project learning files. It supports recurring review and promotion of durable AI/model guidance into project memory, model selection matrices, prompt libraries, runbooks, and policy documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files can capture sensitive model inputs, outputs, customer data, PII, API keys, or model access tokens if users log raw details.

Mitigation: Keep learning files out of version control unless reviewed, redact sensitive excerpts, and avoid logging secrets, customer data, or PII.

Risk: Optional hooks can add persistent reminders across sessions and may inspect command output when enabled.

Mitigation: Enable hooks only per project with narrow matchers, and use the PostToolUse detector only when command-output inspection is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jose-compu/skills/self-improving-ai)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [OpenClaw Hook](hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local learning files and optional project-scoped hook guidance; users should review entries before promotion.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
