## Description:

Guides developers in converting PyPI packages into Rez packages with rez-pip, selecting the target Python version and repository, and troubleshooting failed conversions or resolves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make PyPI dependencies available as Rez packages and diagnose packages that fail to resolve after conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversions can write packages to a shared release repository or an unintended custom prefix.

Mitigation: Confirm the destination repository before conversion; use shared or release paths only when publication is intended.

Risk: A converted package may exist but fail to resolve in the intended Python environment.

Mitigation: Pin the target Python version and verify both package discovery and a real Rez resolve after conversion.

## Reference(s):

- [rez-pip-integration on ClawHub](https://clawhub.ai/loonghao/skills/rez-pip-integration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with Bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes repository selection and resolve-verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
