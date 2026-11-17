## Description:

Analyzes Taobao and Tmall product reviews to extract authentic customer feedback, quality issues, and product selling points for e-commerce sellers, product selection analysis, and market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and market researchers use this skill to analyze public Taobao/Tmall product review feedback, compare competing products, identify common complaints, and surface product strengths. The output is intended as advisory analysis rather than a definitive quality assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retrieve public Taobao/Tmall review data.

Mitigation: Use it only with explicit product URLs or clearly identified products and confirm that the resulting analysis is appropriate for the intended business decision.

Risk: The Python dependencies are not pinned.

Mitigation: Install dependencies in a virtual environment and review package versions before use.

Risk: Review analysis may be incomplete or misleading when based on public or sampled review data.

Mitigation: Treat reports as advisory and validate important findings against source reviews or independent evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/275254cl-hash/skills/taobao-review-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with review metrics, sentiment summary, keyword extraction, issue ranking, selling points, competitive comparison, and improvement suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require python3, curl, and Python packages requests and jieba; may retrieve public Taobao/Tmall review data for explicit product URLs or clearly identified products.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
