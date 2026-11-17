## Description:

Fast OSINT and reconnaissance presets using bbot and nmap. One-command subdomain enumeration, port scanning, and web fingerprinting for bug bounty recon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized security testers use this skill to run bug bounty reconnaissance presets for subdomain enumeration, port scanning, web probing, and passive OSINT collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform active reconnaissance and port scanning against external targets.

Mitigation: Run it only against targets you are authorized to test and confirm program scope before scanning.

Risk: Target and output path safeguards are weak.

Mitigation: Use a restricted workspace or container and avoid untrusted target strings until output path handling is fixed.

Risk: The bbot dependency is installed externally and may change over time.

Mitigation: Pin or review the bbot version before installation and deployment.

## Reference(s):

- [Recon Quick on ClawHub](https://clawhub.ai/hostilespider/skills/recon-quick)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown instructions with bash commands; generated reconnaissance outputs may be text files or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bbot and nmap; writes reconnaissance results under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
