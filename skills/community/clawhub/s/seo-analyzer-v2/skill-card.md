## Description:

SEO Analyzer Pro analyzes a public webpage for title, meta description, H1 usage, and content length, then returns an SEO score with optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:


## Use Case:

Developers, marketers, and site owners use this skill to ask an agent to inspect a public webpage and summarize basic SEO issues. It is useful for quick checks before deeper editorial or technical SEO review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes a credential-like API key.

Mitigation: Remove the key from the release, rotate it, and use a secret manager or runtime configuration before installation.

Risk: The skill fetches arbitrary user-supplied URLs without documented safeguards.

Mitigation: Only analyze public URLs and add validation that blocks localhost, private, link-local, and redirected internal destinations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loverun321/skills/seo-analyzer-v2)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object with score, extracted metadata, issues, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores title, meta description, H1 presence, and content length on a 100-point scale.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
