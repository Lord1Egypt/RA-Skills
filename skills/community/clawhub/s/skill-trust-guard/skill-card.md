## Description:

Enforces skill-trust-scanner security checks before installing skills, blocking or alerting based on risk scores to reduce supply chain threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walkman1w](https://clawhub.ai/user/walkman1w)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to scan skills before installation, block high-risk packages, and require confirmation for medium-risk packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can replace the user's clawhub command path through a PATH shim.

Mitigation: Use it in a controlled environment, review the generated shim path before enabling it, and keep a documented uninstall or repair path.

Risk: The install flow performs broad install and deletion operations.

Mitigation: Validate destination paths before use and avoid running it against untrusted targets until path validation is reviewed.

Risk: The scanner is executed through npx without a pinned runtime package.

Mitigation: Pin scanner execution dependencies or run the scanner from a reviewed local checkout before using the wrapper for production installs.

Risk: Artifact identity binding is not proven by the provided evidence.

Mitigation: Confirm the artifact being scanned is the exact artifact being installed before relying on the install decision.

## Reference(s):

- [Skill Trust Guard on ClawHub](https://clawhub.ai/walkman1w/skills/skill-trust-guard)
- [Publisher profile](https://clawhub.ai/user/walkman1w)
- [README.md](artifact/README.md)
- [TEST_REPORT.md](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces allow, warn, or reject decisions from scan scores; installation may require interactive confirmation unless --yes is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
