## Description:

Audits GitHub repositories for security vulnerabilities, malicious code patterns, dependency risks, license concerns, and suspicious behavior, then generates a security report and may scaffold a clean reimplementation after safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erickgrau](https://clawhub.ai/user/erickgrau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to assess third-party GitHub repositories before adoption, forking, dependency use, or clean reimplementation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles untrusted repositories in ways that can copy or overwrite host files.

Mitigation: Run only in a disposable sandbox or container with no host credentials, and use a trusted output directory outside the repository.

Risk: The skill may invoke GitHub, npm, Snyk, or other network-backed scans without clear consent.

Mitigation: Require explicit opt-in before network-backed scans and avoid the unpinned pip install step.

Risk: The authoritative security verdict for this release is suspicious.

Mitigation: Review the skill before installing or running it against untrusted or private repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erickgrau/skills/repo-security-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON risk assessments, shell commands, and scaffolded project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save audit outputs, raw scan findings, inventory files, and clean reimplementation scaffolds when the reviewed repository passes safety checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
