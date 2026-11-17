## Description:

True Seeing audits verifiable facts in AI-generated articles with web search, produces a discrepancy report, and applies only user-approved factual corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[francisk](https://clawhub.ai/user/francisk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and editors use True Seeing to fact-check AI-generated Chinese articles, generate verification reports, and apply user-selected factual corrections with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article claims are sent to web search during verification.

Mitigation: Use the skill only with content appropriate for external search, and avoid submitting sensitive or non-public article claims.

Risk: Search results can come from blogs, social media, unfamiliar sites, mirrors, or conflicting sources.

Mitigation: Review source quality and the discrepancy report before accepting any correction.

Risk: The skill does not replace expert review for legal, medical, or other specialist factual claims.

Mitigation: Route high-stakes domain claims to qualified reviewers before publication or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/francisk/skills/true-seeing)
- [README](artifact/README.md)
- [Fact extraction rules](artifact/fact-extraction-rules.md)
- [Search query templates](artifact/search-query-templates.md)
- [Verification criteria](artifact/verification-criteria.md)
- [Evaluation cases](artifact/eval-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON fact lists and verification reports; Markdown discrepancy reports and corrected articles with citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits extraction to 30 facts, verifies in batches of five, and pauses for user approval before replacing corrected facts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
