## Description:

Fetch a single X tweet or X Article with charge-first billing (0.001 USDT/call).

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangkefeng-ai](https://clawhub.ai/user/huangkefeng-ai)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve the content of one X status URL or one X Article URL from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill bundles billing authority and charges before fetching content.

Mitigation: Review pricing and billing behavior before use; remove or rotate the embedded billing credential and require an operator-provided credential.

Risk: The skill sends user identifiers and requested URLs to external services and can fetch arbitrary runtime URLs.

Mitigation: Use it in a constrained environment, add URL validation for expected X URLs, and disclose third-party data sharing before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing fetched tweet or article content; billing failures may emit PAYMENT_URL text on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches one X status URL or one X Article URL per run; fallback tweet text is capped at 12000 characters and article text at 50000 characters.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
