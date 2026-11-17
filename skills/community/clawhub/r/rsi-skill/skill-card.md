## Description:

Evaluate a prompt, system prompt, skill instruction, or agent instruction against test cases, then iteratively improve it with an open model while checking that held-out cases do not regress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandeep85das](https://clawhub.ai/user/sandeep85das)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to measure prompts and agent instructions against concrete cases, then keep revisions only when training scores improve without reducing held-out scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and test cases are sent to the selected model endpoint, and endpoint selection can prioritize an existing OPTIQ_CLOUD_KEY.

Mitigation: Check which endpoint will be used and send private material only to an endpoint you trust.

Risk: Remote model calls may incur API costs, and locally saved results may contain prompts or model outputs.

Mitigation: Consider call costs and protect saved evaluation results.

Risk: A proposed revision may be incorrect or misleading despite a higher score on the supplied cases.

Mitigation: Review proposed changes before approving or applying them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sandeep85das/skills/rsi-skill)
- [GSM8K worked example](references/example-gsm8k.md)
- [GSM8K dataset](https://huggingface.co/datasets/openai/gsm8k)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands]

**Output Format:** [Prompt revisions and evaluation results in Markdown and JSON, with shell commands for running evaluations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores depend on the supplied test cases and model responses; a run samples each case once.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
