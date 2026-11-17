## Description:

Search hashes through 25 billion leaked passwords using the Weakpass API (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibnaleem](https://clawhub.ai/user/ibnaleem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and authorized auditors use this skill to query Weakpass for hash lookups, hash-prefix ranges, generated wordlists, and available wordlist data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends password-related hash material or wordlist inputs to an external API.

Mitigation: Use it only for authorized password-auditing work and avoid submitting production secrets unless policy explicitly allows it.

Risk: Directly substituting generated or user-supplied values into curl commands can be unsafe.

Mitigation: Prefer URL-encoded structured HTTP calls and review generated shell commands before execution.

## Reference(s):

- [Weakpass](https://weakpass.com/)
- [Weakpass API](https://weakpass.com/api)
- [Weakpass OpenAPI JSON](https://weakpass.com/openapi.json)
- [Weakpass OpenAPI YAML](https://weakpass.com/openapi.yaml)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and calls an external Weakpass API; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
