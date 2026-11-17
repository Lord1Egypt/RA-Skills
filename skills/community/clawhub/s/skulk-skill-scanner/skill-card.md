## Description:

Scan OpenClaw skill folders for security red flags before installing or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adainthelab](https://clawhub.ai/user/adainthelab)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect OpenClaw skill folders before installation or publication and identify common security red flags such as exfiltration patterns, credential access, destructive commands, obfuscation, privilege escalation, and supply chain risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads eligible files under the user-specified target path to analyze their contents.

Mitigation: Run it only against skill folders intended for inspection, not broad personal or sensitive directories.

Risk: Static pattern matching can miss sophisticated, runtime-generated, or context-dependent unsafe behavior.

Mitigation: Treat scanner results as a first-pass signal and manually review skills before granting sensitive access.

## Reference(s):

- [Skulk Skill Scanner on ClawHub](https://clawhub.ai/adainthelab/skills/skulk-skill-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner output may include pass, warn, or fail verdicts, severity-grouped findings, scores, file paths, and line references.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
