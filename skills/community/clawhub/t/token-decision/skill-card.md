## Description:

Analyzes a prompt, classifies the task, recommends a cost-effective Chinese large language model, and can execute the prompt while tracking token usage and estimated cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaoxuan2026](https://clawhub.ai/user/nihaoxuan2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to choose an LLM for writing, coding, translation, analysis, Q&A, summarization, math reasoning, or chat based on quality, cost, latency, context length, and token-budget estimates. It can return a recommendation only or call the selected model provider when execution is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt content may be sent to external model providers during execution.

Mitigation: Use --dry-run or --no-exec when only a routing recommendation is needed, and do not submit confidential prompts unless provider sharing is approved.

Risk: Prompt snippets are stored locally in plaintext usage logs.

Mitigation: Disable raw prompt logging or regularly clear the local usage database before using the skill with sensitive data.

Risk: The skill makes telemetry calls that may not be obvious to users.

Mitigation: Remove or disable CountAPI telemetry before deployment in environments with privacy, compliance, or disclosure requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nihaoxuan2026/skills/token-decision)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown-style console output with model recommendations, cost estimates, token estimates, alternatives, and optional model response text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports cheap, balanced, and quality modes; --dry-run and --no-exec avoid model execution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
