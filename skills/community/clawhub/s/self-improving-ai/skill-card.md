## Description: <br>
Captures learnings about GenAI/LLM configuration, model selection, inference optimization, fine-tuning, RAG pipelines, prompt engineering, multimodal processing, and cost management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI engineers use this skill to capture recurring model behavior, prompt patterns, inference problems, RAG issues, evaluation findings, and AI capability requests. It helps teams maintain project learning logs and promote proven patterns into model selection, prompt, configuration, or runbook guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture sensitive prompts, customer data, API keys, or model access tokens if users paste raw content into entries. <br>
Mitigation: Record only redacted summaries and metrics; do not store API keys, access tokens, customer data, raw sensitive prompts, or PII. <br>
Risk: Global or broad prompt hooks can create reminders across projects where AI learning capture was not intended. <br>
Mitigation: Use project-level hooks with AI-specific matchers and enable global hooks only when cross-project reminders are intentional. <br>
Risk: Promoting learnings into AGENTS.md, SOUL.md, TOOLS.md, or model configuration files can change agent behavior if entries are inaccurate or too broad. <br>
Mitigation: Review proposed promotions and model configuration changes before applying them to shared project guidance. <br>


## Reference(s): <br>
- [Self-Improving AI ClawHub Page](https://clawhub.ai/jose-compu/self-improving-ai) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and optional generated skill scaffold files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Opt-in hooks can emit short reminder blocks; persistent entries are written to local .learnings files only when the user or agent records them.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
