## Description:

Verify Zambo execution receipts. Every Zambo tool response includes a verifiable AER-1 receipt with an id, timestamp, and SHA-256 output digest. Use when you need to check that a Zambo tool call ran and that the saved result was not changed since it was saved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zambodotdev](https://clawhub.ai/user/zambodotdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check that a Zambo tool call has a receipt and that the saved output matches its recorded digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt pages may be public and expose tool arguments.

Mitigation: Keep secrets out of Zambo tool arguments.

Risk: A matching digest does not establish that the underlying data is correct or who authorized the call.

Mitigation: Treat verification as an integrity check and assess the source and authorization separately.

Risk: AER-1 is an individual Internet-Draft, not an IETF-endorsed standard.

Mitigation: Describe AER-1 as an Internet-Draft and avoid implying standards endorsement.

Risk: The included Python sample needs its JSON parsing corrected before use.

Mitigation: Correct the sample's response parsing and verify it against the endpoints before relying on it.

## Reference(s):

- [AER-1 Internet-Draft](https://datatracker.ietf.org/doc/draft-zambo-aer1/)
- [Zambo receipt verifier](https://zambo.dev/verify/)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, JSON]

**Output Format:** [Markdown guidance with a JSON receipt example and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checks for receipt status, timestamp, and the digest of the exact saved output text.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
