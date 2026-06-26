## Description: <br>
Checks Python library compatibility with HarmonyOS by downloading source from GitHub/PyPI, detecting Windows-specific dependencies, running pytest, and generating compatibility reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryKing1992](https://clawhub.ai/user/terryKing1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess whether Python packages or requirements files are suitable for HarmonyOS deployment by checking platform-specific dependencies, running available tests, and reviewing generated compatibility reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs third-party Python package code and tests locally. <br>
Mitigation: Run it only in a disposable, low-privilege environment with no secrets in environment variables; do not use sudo or administrator privileges. <br>
Risk: Untrusted package names or requirements files can cause unsafe local execution paths. <br>
Mitigation: Avoid using it on untrusted package names or requirements files, and review package sources before running compatibility checks. <br>
Risk: Compatibility reports may be incomplete, environment-dependent, or advisory rather than authoritative. <br>
Mitigation: Review generated reports manually, distinguish environment failures from code failures, and validate findings in the target HarmonyOS environment. <br>


## Reference(s): <br>
- [Python Environment Setup on HarmonyOS](artifact/references/python-env-setup.md) <br>
- [Python Package Compatibility Database for HarmonyOS](artifact/references/compatibility-database.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/terryKing1992/python-harmony-compatibility-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON compatibility reports with advisory text and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include per-package compatibility status, pytest results, environment issue classification, and platform dependency findings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
