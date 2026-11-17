## Description:

Environment diagnostic skill for the SenseNova-Skills project that checks sn-image-base installation, Python dependencies, environment variables, and reload readiness before other skills run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers maintaining SenseNova-Skills use this skill to diagnose local setup issues, configure required SenseNova environment variables, and confirm the environment is ready before image-related skills run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Doctor output may expose resolved API configuration or credentials in plain text.

Mitigation: Review the output before sharing logs, redact API keys and tokens, and prefer secure secret storage over plaintext .env files where possible.

Risk: The documentation may not fully match the script's actual behavior.

Mitigation: Review the script and its output in the target environment before relying on the diagnostic result.

Risk: The skill can prompt for environment variables and save accepted values to a .env file.

Mitigation: Confirm the destination file and stored values before continuing, and avoid committing or distributing generated .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-image-doctor)
- [sn-image-base skill documentation](sn-image-base/SKILL.md)
- [sn-image-base API specification](sn-image-base/references/api_spec.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text diagnostics with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt for missing environment variables and save accepted values to a .env file.]

## Skill Version(s):

2026.9.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
