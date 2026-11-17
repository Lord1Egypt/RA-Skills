## Description:

Convert URL to PDF suitable for mobile reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to render a supplied webpage URL as a mobile-readable PDF and return the generated file path for delivery to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URLs may expose local or private-network pages reachable from the agent host.

Mitigation: Run the skill in a sandbox with restricted outbound network access and no access to local or private services; allow only trusted public URLs.

Risk: Generated PDFs may overwrite files at the selected output path.

Mitigation: Use an isolated output directory and check the destination path before returning or sharing the generated file.

Risk: Runtime dependencies may change because production pinning is not provided by the artifact.

Mitigation: Pin dependencies and browser versions before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/url2pdf)
- [ClawHub homepage metadata](https://clawhub.ai/guoqiao/url2pdf)
- [Usage examples](https://github.com/guoqiao/skills/tree/main/url2pdf/examples)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF file path on stdout with Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PDFs are written to the configured output path, defaulting to the user's Documents directory.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
