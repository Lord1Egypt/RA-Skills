## Description:

Analyzes user-provided text for sentiment and emotions through AIProx's sentiment-analysis service, with each call costing 50 sats via Bitcoin Lightning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users can analyze one text at a time and receive its overall sentiment, score, emotions, and reasoning. Each paid call requires user approval at 50 sats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text and payment credentials are sent to AIProx and its AI provider; provider retention has not been independently audited.

Mitigation: Submit only text you are comfortable sharing, exclude secrets and personal information, and never expose the spend token in output or request text.

Risk: Each analysis costs 50 sats, and a spend token can authorize payment.

Mitigation: Get user approval before each paid call and use a minimally funded token or per-call L402 payment.

## Reference(s):

- [AIProx documentation](https://aiprox.dev/docs.html)
- [AIProx service](https://aiprox.dev)
- [LightningProx top-up](https://lightningprox.com/topup)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [Structured JSON sentiment result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One text per call; result may include sentiment, score, magnitude, emotions, reasoning, confidence, mode, and context.]

## Skill Version(s):

2.0.0 (source: frontmatter, changelog, released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
