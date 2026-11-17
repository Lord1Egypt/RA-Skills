## Description:

Host-based Linux incident response and remediation skill focused on precise threat detection, forensic-safe data collection, firewall control, integrity validation, and controlled remediation while preserving system stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiaraho](https://clawhub.ai/user/kiaraho)

### License/Terms of Use:


## Use Case:

Security engineers, system administrators, and incident responders use this skill to analyze Linux hosts during suspected compromise, collect evidence safely, inspect network, process, integrity, and authentication signals, and apply controlled containment or remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged remediation commands can disrupt access or services if applied to the wrong host, interface, process, or firewall backend.

Mitigation: Verify current state before and after changes, preserve management access, prefer narrow reversible commands, and document each action.

Risk: The skill references installing remote forensic scripts from mutable GitHub URLs.

Mitigation: Pin exact commits, verify checksums or signatures, download as an unprivileged user, and prefer a trusted internal forensic toolkit or disposable analysis VM.

Risk: Rootkit, malware, and audit tools can produce false positives or increase system load during live response.

Mitigation: Scope scans carefully, validate findings manually before destructive actions, and preserve hashes and timestamps for evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiaraho/skills/sys-guard-linux-remediator)
- [Didier Stevens Suite](https://github.com/DidierStevens/DidierStevensSuite)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux host incident-response recommendations and commands; execution requires operator review and appropriate privileges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
