## Description:

PMs use this skill to run a structured PRD review workflow after PRD v1.0, coordinating backend, frontend, QA, and design reviews through gated iterations until a coding-ready v3.x draft is reached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mistyhuqwq-art](https://clawhub.ai/user/mistyhuqwq-art)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and product teams use this skill to organize parallel PRD review across technical, QA, and design perspectives, classify feedback, route must-clarify items to business owners, and converge on a final PRD suitable for acceptance and coding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may invoke the workflow outside an explicit PRD-review context or lead to product documents and logs being changed prematurely.

Mitigation: Invoke the skill only for explicit PRD-review work and confirm before updating PRDs, review logs, or decision records.

Risk: Unresolved must-clarify items can be incorrectly treated as assumptions in the final PRD.

Mitigation: Require a business-owner decision for each must-clarify item before writing the decision back into the PRD.

## Reference(s):

- [PRD template](../../templates/prd-template.md)
- [PM lessons](../../lessons/by-role/pm.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, JSON]

**Output Format:** [Markdown guidance with checklist, review-message, feedback-list, and JSON log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; security evidence found no code, install scripts, credential handling, network access, or persistence behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
