## Description:

Check Python library compatibility with HarmonyOS by downloading source from GitHub or PyPI, detecting Windows-specific dependencies, running pytest, and generating compatibility reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryking1992](https://clawhub.ai/user/terryking1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether Python packages are suitable for HarmonyOS deployment. It reports installation status, platform-specific dependency findings, pytest results, and compatibility conclusions for one or more packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can download and execute third-party package code with broad local access.

Mitigation: Run it only in a disposable, low-privilege container or VM with no secrets, no sensitive host directories mounted, and constrained network access.

Risk: Compatibility reports may overstate or understate real HarmonyOS readiness.

Mitigation: Treat reports as advisory and review failed tests, environment issues, and package-specific constraints before deployment decisions.

Risk: Suggested privileged package installation commands can increase host exposure.

Mitigation: Do not run suggested sudo pip commands for arbitrary packages; prefer isolated environments and least-privilege package installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryking1992/skills/python-harmony-compatibility-checker)
- [Python Environment Setup on HarmonyOS](artifact/references/python-env-setup.md)
- [Python Package Compatibility Database for HarmonyOS](artifact/references/compatibility-database.md)
- [Example numpy Compatibility Report](artifact/compatibility_report_numpy-2.2.1_20260309_234148.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown and JSON compatibility reports, with terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include package status, pass rates, detected platform dependencies, per-test-case results, and advisory recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact manifest reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
