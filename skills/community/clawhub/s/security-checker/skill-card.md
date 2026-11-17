## Description:

Security Checker scans Python skill files before ClawHub publishing for dangerous imports, hardcoded secrets, unsafe file operations, and unsafe functions such as eval, exec, and subprocess.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

Developers and skill publishers use Security Checker to statically review Python skill files before publishing to ClawHub and identify risky patterns that need manual review or remediation. It should be used as an advisory scanner unless its fail-open gate behavior is fixed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated commit or publish gates can pass even when warnings or scan errors occur.

Mitigation: Use the scanner as advisory, manually review its output, and fix the exit-code behavior before relying on it to block commits or releases.

Risk: Static pattern matching cannot determine whether every flagged construct is legitimate or whether sophisticated unsafe code is present.

Mitigation: Pair scan results with manual code review, isolated testing, and additional Python security tools where appropriate.

## Reference(s):

- [Security Checker ClawHub page](https://clawhub.ai/johstracke/skills/security-checker)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal scan results with warning lines and summary status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis only; results require manual review, and documented automated gates should not be treated as blocking until the exit-code behavior is fixed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
