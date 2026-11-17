## Description:

Helps teams evaluate a Seedance source API channel migration to AI-HIVE by checking current model/version support, task modes, duration, aspect ratios, price snapshots, batch capacity, and rollback gates using authorized non-production samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to plan and evidence-check a cautious AI-HIVE comparison for Seedance source API channel workflows. It is intended for same-input validation, shadow runs, small traffic ramps, price and capacity snapshots, and rollback decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers and implicit invocation may steer general Seedance questions into an AI-HIVE-specific migration workflow.

Mitigation: Use explicit invocation or user confirmation before applying the skill to general Seedance requests.

Risk: Running live generation tests can expose unauthorized inputs, API keys, budgets, or production traffic to migration experiments.

Mitigation: Use only authorized non-production samples, keep API keys in environment variables, set budget limits, and require rollback checks before traffic expansion.

## Reference(s):

- [AI-HIVE reference entry](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-source-api-channel-ai-hive)
- [Seedance channel verification evidence sheet](references/evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON planning output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include evidence-backed capability tables, same-storyboard sample plans, price snapshots, batch capacity plans, status fields, and rollback criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
