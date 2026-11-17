## Description:

Semantic security scanner for OpenClaw skills that detects prompt injection, data exfiltration, and hidden instructions traditional code scanners miss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fermionoid](https://clawhub.ai/user/fermionoid)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use Senseguard to scan OpenClaw skill directories for natural-language security threats, suspicious instructions, and risky skill behavior before installation or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can read local skill directories and retain scan results in a local cache.

Mitigation: Run it only against intended skill directories, avoid untrusted paths that may contain symlinks or secret-bearing files, and review or clear the cache as needed.

Risk: Semantic checks may be incomplete or fail open, so a SAFE rating is not proof that semantic analysis occurred.

Mitigation: Use Layer 2 in an isolated tool-less review context for higher-risk skills and treat the report as review input rather than a final safety decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fermionoid/skills/senseguard)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown risk report with optional raw JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a score, SAFE/CAUTION/DANGEROUS/MALICIOUS rating, findings, evidence snippets, line numbers, and recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
