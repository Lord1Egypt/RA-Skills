## Description:

Security audit tool for AI agent skills. Scans skill packages for malware, credential theft, and suspicious patterns before installation. Defensive security tool with optional enterprise reporting (user-controlled destination).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit AI agent skill packages, archives, or release bundles before installation. It supports scanning for suspicious behavior such as credential access, data exfiltration, code injection patterns, Unicode steganography, and process manipulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on downloading and running an externally hosted compiled binary that was not included in the reviewed package.

Mitigation: Review before installing, independently verify the binary checksum and source provenance, or build from source before execution.

Risk: Scanning broad private directories can expose more local file content than intended to generated reports.

Mitigation: Limit scans to the specific skill package or release bundle that needs review.

Risk: The optional upload URL and external-engine options can send report data outside the local machine.

Mitigation: Use upload and external-engine options only with trusted destinations and after confirming what report data may leave the machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyzlmh/skills/skillscan-wrapper)
- [Gitee source repository](https://gitee.com/random_player/cmic-skill-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and scanner report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local scan reports in a user-specified output directory and may optionally upload reports only when the user provides an upload URL.]

## Skill Version(s):

0.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
