## Description:

Provides guidance for running PowerShell scripts in a constrained sandbox with command allowlisting, timeout control, output limits, and pre-execution checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to plan constrained PowerShell execution, tune sandbox parameters, and understand expected command, timeout, output, and file-access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package claims to run untrusted PowerShell safely, but the authoritative security evidence says the core sandbox implementation is missing.

Mitigation: Do not use it for untrusted scripts until the real implementation is included, tested end to end, and reviewed under an operating-system isolation model.

Risk: Artifact documentation and test results claim security readiness without matching implementation evidence in the packaged files.

Mitigation: Treat the documentation and test results as unverified claims; require review of the actual sandbox script and tests before deployment.

Risk: Network access and allowlist customization can broaden what executed scripts are able to do.

Mitigation: Keep network access disabled by default, keep command allowlists minimal, and run PowerShell workloads inside an isolated Windows environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-powershell-sandbox)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Artifact Test Results](artifact/TEST_RESULTS.md)
- [Artifact Package Metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timeout, output limit, working directory, network access, and command allowlist recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact package.json, artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
