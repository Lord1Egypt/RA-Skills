## Description:

Preflight-check Render service environment variables before deploys; catches missing keys and placeholder/template values that commonly break production rollouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and deployment engineers use this skill to check Render service environment variables before deploys, especially when missing keys, placeholder values, or ambiguous service selection could break a rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-configured API base URL could receive the Render API key.

Mitigation: Use the default Render HTTPS API endpoint or strictly allowlist trusted Render API origins before running the script.

Risk: API JSON handling could accidentally execute API responses as Python code.

Mitigation: Patch or review the script so API responses are passed to Python through a data file descriptor or temporary file, separate from Python source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/render-env-guard)
- [Render API v1](https://api.render.com/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal report with PASS/FAIL lines and exit status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exit code 0 when required keys are valid and exit code 1 when lookup or validation fails.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
