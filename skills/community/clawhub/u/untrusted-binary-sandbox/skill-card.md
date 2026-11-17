## Description:

Use when asked to safely inspect, sandbox, detonate, run, or dynamically observe untrusted release artifacts, closed-source binaries, JARs, installers, wallet/private-key software, crypto trading bots, or suspicious GitHub releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[remixmm](https://clawhub.ai/user/remixmm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to plan staged static and dynamic observation of untrusted binaries, installers, JARs, wallet software, trading bots, and suspicious releases. It helps capture evidence, constrain execution, and report confirmed behavior, risks, unknowns, and wallet/key exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated sandbox files can be mistaken for a complete malware-analysis boundary.

Mitigation: Treat generated scaffolds as a starting point, pin container images by digest where possible, and use a disposable VM or VPS for hostile samples.

Risk: Dynamic execution of untrusted artifacts can expose host secrets, funded wallets, cloud credentials, or production environment files.

Mitigation: Require explicit approval before running any sample, use non-production environments, and keep real secrets, browser profiles, SSH keys, cloud credentials, and funded wallets out of the sandbox.

Risk: Network-enabled observation can allow unexpected egress, payload download, or transaction activity.

Mitigation: Start with offline or internal-only tiers, enable controlled egress only after earlier tiers are clean, and log DNS, endpoints, files, processes, and wallet/key behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/remixmm/skills/untrusted-binary-sandbox)
- [Docker and VM sandbox reference](artifact/references/docker-sandbox.md)
- [Observation checklist and report template](artifact/references/observation-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Docker, Docker Compose, mock RPC, and runbook files when scaffolding is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scaffold script writes files but does not execute the sample by default; dynamic execution and network access require explicit approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
