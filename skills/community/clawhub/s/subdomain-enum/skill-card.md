## Description:

Enumerate subdomains for any domain using DNS brute-force and certificate transparency logs (crt.sh).

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and authorized infrastructure owners use this skill to discover subdomains, map exposed services, and audit a domain's attack surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subdomain enumeration can create unauthorized reconnaissance activity when run against domains the user does not control.

Mitigation: Use the skill only for domains the user owns or has explicit permission to test.

Risk: crt.sh lookup sends the target domain to a third-party public certificate transparency service.

Mitigation: Use the DNS-only option when third-party lookup disclosure is unacceptable for a confidential target.

Risk: The Python requests dependency is required and may vary across environments.

Mitigation: Pin and review the dependency version in controlled or commercial environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/subdomain-enum)
- [crt.sh certificate transparency lookup](https://crt.sh/?q=%.{domain}&output=json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files]

**Output Format:** [Human-readable terminal report or JSON, with optional saved result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are deduplicated across DNS brute-force and crt.sh sources; DNS concurrency, timeout, wordlist, JSON output, file output, and crt.sh usage are configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
