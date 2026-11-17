## Description:

Shuffle repetitive JSON objects safely by validating schema consistency before randomising entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to validate flat JSON object collections and return a safely shuffled version without breaking JSON syntax or schema consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shuffling records can change meaning when JSON order carries business or workflow significance.

Mitigation: Use the skill only where record order can safely change and review the shuffled output before replacing original data.

Risk: Nested objects or inconsistent properties can produce unsafe or misleading output in the default mode.

Mitigation: Validate syntax and schema consistency first; stop and report inconsistencies unless explicit overrides describe how to handle them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhauga/skills/shuffle-json-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON with concise validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves JSON validity and original formatting conventions when returning shuffled data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
