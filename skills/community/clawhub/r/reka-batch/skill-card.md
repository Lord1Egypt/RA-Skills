## Description:

Runs large, non-urgent sets of independent language model requests through Reka's Batch API, with results promised within 24 hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reka-ai](https://clawhub.ai/user/reka-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to label, enrich, translate, summarize, or transform many independent items when the work can run asynchronously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch submissions can incur charges, and the security review says the spend approval gate is unconfirmed.

Mitigation: Before submitting, review the row count and cost estimate and obtain approval for the spend.

Risk: The skill uses a REKA_API_KEY and notification commands; the security review flags command and environment handling.

Mitigation: Keep the API key out of command arguments and logs, and inspect notification commands before use.

Risk: Scanner coverage is incomplete, and some static checks could not fully evaluate the skill.

Mitigation: Review the full skill bundle, the selected external model, and notification behavior before deployment.

## Reference(s):

- [Reka Batch API overview](https://developer.reka.ai/batch)
- [Reka Batch API reference](https://developer.reka.ai/batch/reference)
- [Reka pricing](https://developer.reka.ai/pricing)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [JSONL request and result files, JSON summaries, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Independent request rows; collected results include per-row success or error information.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
