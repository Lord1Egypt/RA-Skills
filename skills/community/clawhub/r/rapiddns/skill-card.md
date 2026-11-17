## Description:

DNS reconnaissance and subdomain enumeration using rapiddns-cli and the RapidDNS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapiddns](https://clawhub.ai/user/rapiddns)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and authorized researchers use this skill to run RapidDNS searches for subdomains, DNS records, reverse IP results, CIDR enumeration, advanced queries, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install commands may download an unverified remote executable and move it into a system-wide path.

Mitigation: Review install commands before execution, prefer a user-local install, pin a reviewed version, and verify checksums or signatures when available.

Risk: Using @latest can reduce reproducibility and make reviewed behavior drift over time.

Mitigation: Pin a specific rapiddns-cli version that has been reviewed for the intended environment.

Risk: The RapidDNS API key is a sensitive credential.

Mitigation: Store and handle the API key as a secret, avoid exposing it in logs or shared command history, and rotate it if disclosure is suspected.

Risk: DNS reconnaissance workflows can be misused against domains, IPs, or networks without authorization.

Mitigation: Use the skill only for assets the operator is authorized to investigate.

## Reference(s):

- [RapidDNS API Reference](references/api.md)
- [RapidDNS](https://rapiddns.io)
- [RapidDNS CLI Releases](https://github.com/rapiddns/rapiddns-cli/releases/latest)
- [ClawHub Skill Page](https://clawhub.ai/rapiddns/skills/rapiddns)
- [ClawHub Publisher Profile](https://clawhub.ai/user/rapiddns)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call rapiddns-cli and produce JSON, CSV, or text output through the RapidDNS service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
