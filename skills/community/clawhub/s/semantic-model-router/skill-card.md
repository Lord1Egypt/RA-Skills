## Description:

Smart LLM Router routes each query to the cheapest capable model across Anthropic, OpenAI, Google, DeepSeek, and xAI using a local classifier, semantic fallback, and keyword rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayray1218](https://clawhub.ai/user/rayray1218)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to route LLM requests into basic, balanced, or elite model tiers and compare expected model cost for a prompt. It can be used from Python code or a CLI workflow when selecting among supported model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routed prompts may be saved locally in plaintext query history.

Mitigation: Disable or redirect local history before use, document the storage path and deletion process, and avoid routing secrets, proprietary code, customer data, or regulated information.

Risk: Dependency and model artifact retrieval risks are under-disclosed.

Mitigation: Pin and verify dependencies and any retrieved model artifacts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rayray1218/skills/semantic-model-router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python dictionaries, plain text CLI reports, and Markdown examples with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes one prompt at a time and writes local query history by default unless configured otherwise.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
