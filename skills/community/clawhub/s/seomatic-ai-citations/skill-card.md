## Description:

Helps site owners assess whether AI answers cite their site by analyzing logged-in answer observations, AI crawler fetches, AI referrals, and published brand facts in SEOmatic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minh42](https://clawhub.ai/user/minh42)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners and marketers use this skill to understand where AI systems cite or use their pages and to investigate inaccurate AI statements about their business. It prioritizes logged-in observed answers when available and identifies server-side scan results as de-personalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is incomplete because one reference was unavailable; its benign verdict also notes a low-probability agency flag.

Mitigation: Treat findings as incomplete, review the available first-party evidence, and distinguish logged-in observations from de-personalized scans when explaining results.

## Reference(s):

- [SEOMatic](https://app.seomatic.ai)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown natural-language answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes logged-in observations from de-personalized scans and reports only what the available evidence supports.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
