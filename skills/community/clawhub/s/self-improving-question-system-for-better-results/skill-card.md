## Description:

Diagnoses prompt quality and asks targeted clarification questions so an agent can provide more accurate, actionable, and rigorous answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evafan7](https://clawhub.ai/user/evafan7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to improve underspecified prompts before an answer is generated. It is most useful when the request lacks clear output expectations, needed context, constraints, or success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add extra back-and-forth on underspecified prompts.

Mitigation: Use the documented PROCEED ANYWAY option when an answer should be generated from available context.

Risk: Direct prompt-quality challenges can slow simple tasks or feel overly strict when the user already accepts uncertainty.

Mitigation: Apply the enhancement loop only when missing context would materially affect answer quality, and stop after the user declines to add more information.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prompt-quality diagnosis, clarification questions, or direct answer guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to three clarification rounds before answering unless the user chooses to proceed with available context.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
