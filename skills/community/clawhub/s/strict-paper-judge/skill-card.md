## Description:

Strictly judge whether a research paper is worth following, reading, or recommending for paper triage, reviews, literature evaluation, arXiv screening, research taste checks, and deciding whether a method is genuinely valuable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[197895](https://clawhub.ai/user/197895)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, engineers, and technical reviewers use this skill to triage research papers and decide whether a method has enough originality, empirical strength, and influence potential to follow or recommend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is deliberately skeptical and may produce a hard value judgment instead of a neutral paper summary.

Mitigation: Use it for strict paper triage or review decisions, and request a separate neutral summary when that is the desired output.

Risk: The workflow expects related-work searches, so conclusions can depend on the quality and freshness of retrieved comparison material.

Mitigation: Review cited related work and baselines before relying on the final recommendation for high-impact decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted research paper evaluation with a conclusion, rating, related-work comparison, originality assessment, limitations, influence estimate, and final judgment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires related-work search and intentionally applies a skeptical evaluation standard.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
