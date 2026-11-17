## Description:

Looks up TON blockchain wallet balances, address information, and token holdings using TonScan's public API with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfeldmann](https://clawhub.ai/user/mariusfeldmann)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to check TON wallet balances, inspect address status, convert nanotons to TON, and produce user-readable wallet balance results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a TON address contacts TonScan and can associate that address lookup with the user's context.

Mitigation: Query only addresses the user explicitly wants checked, avoid submitting addresses that should not be shared with TonScan, and include a short privacy notice in updated releases.

Risk: The skill depends on a free public API that may rate limit requests or return transient errors.

Mitigation: Use retry logic with exponential backoff for 429 and 5xx responses, and validate address formats before making requests.

## Reference(s):

- [TonScan address information API](https://api.tonscan.com/api/bt/getAddressInformation?address={ADDRESS})
- [ClawHub skill release page](https://clawhub.ai/mariusfeldmann/skills/tonscan-address-balance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live TonScan API calls and TON balance values converted from nanotons for display.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
