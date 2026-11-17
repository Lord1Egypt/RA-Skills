## Description:

Validate emails, URLs, phones, dates, and custom patterns. Use when sanitizing input, verifying form fields, checking formats, or enforcing rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Validator to check common input formats and file syntax before accepting or processing user-supplied data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON and YAML file validation can execute unintended commands when given crafted filenames.

Mitigation: Review and fix filename handling before broad deployment, and avoid validating untrusted JSON or YAML filenames.

Risk: URL and domain validation may make outbound network requests.

Mitigation: Run in a constrained environment and disable or isolate network access when checking untrusted URLs or domains.

Risk: Credit-card validation accepts payment card numbers on the command line.

Mitigation: Use only test card numbers and avoid entering real payment card data.

## Reference(s):

- [Validator on ClawHub](https://clawhub.ai/xueyetianya/skills/validator)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform HTTP status checks for URLs when curl is available and DNS lookups for domains when dig is available.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
