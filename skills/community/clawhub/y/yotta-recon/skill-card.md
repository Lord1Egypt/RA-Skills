## Description:

Yotta-Recon identifies open ports, services, and version fingerprints for asset inventory and authorized security testing, producing text, JSON, or Markdown results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers and security teams use the skill to inventory authorized targets, identify exposed ports and common services, and produce reconnaissance reports. Fingerprint risk hints need manual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags authorization flaws that may allow probing beyond the approved scope.

Mitigation: Use explicitly approved numeric IPs and a narrow scope file with --no-interactive; avoid --assume-authorized until the flaws are fixed.

Risk: Installer coverage was investigated with mocked connections, so live network behavior and registry package identity remain unverified.

Mitigation: Pin a reviewed installation version and select only the intended agent; verify the package identity before installation.

## Reference(s):

- [Project homepage](https://github.com/YottaMeta/yotta-recon)
- [Scope Guard authorization guidance](references/scope-guard.md)
- [Service fingerprints and risk hints](references/service-fingerprints.md)
- [Protocol probes](references/protocol-probes.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Text tables, JSON results, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include scan details; version-based risk hints require manual verification.]

## Skill Version(s):

0.1.10 (source: SKILL.md frontmatter, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
