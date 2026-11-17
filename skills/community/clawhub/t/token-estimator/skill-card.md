## Description:

Estimates token usage for prompts across Qwen, OpenAI/GPT, Gemini, and fallback character counting, with human-readable and JSON output modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to estimate prompt and response token consumption before sending model requests, compare model-specific tokenization behavior, and request optional compression-savings estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local-only behavior is not guaranteed if tokenizer or dependency loading reaches external package or model sources.

Mitigation: Review before installing, pin dependencies, and pre-cache tokenizer files or force local-only tokenizer loading in a restricted environment.

Risk: Broad triggers may activate the skill more often than intended in an agent workflow.

Mitigation: Review and narrow triggers before enabling the skill in shared or production agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/largetool/skills/token-estimator)
- [SKILL.md](artifact/SKILL.md)
- [Test report](artifact/tests/test-report.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown-style text with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model name, input length, estimated input tokens, output token range, total token range, text type, and optional compression-savings fields.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
