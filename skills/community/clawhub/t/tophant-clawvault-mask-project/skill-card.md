## Description:

Mask sensitive company-project document content before analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martin2877](https://clawhub.ai/user/martin2877)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to mask company names, project amounts, and contextual person names in local project documents before sending sanitized content to an AI model for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom policy files may alter masking behavior and miss sensitive document content.

Mitigation: Use trusted policies and review sanitized output before sharing it with an AI model.

Risk: The skill reads the local document path provided by the user and may write to paths the user provides.

Mitigation: Run it only on user-approved files and choose output paths carefully because existing writable files may be replaced.

Risk: A no-match result does not prove the source document is safe.

Mitigation: Treat no-match warnings as a prompt for manual review or stronger masking rules.

## Reference(s):

- [ClawVault homepage](https://github.com/tophant-ai/ClawVault)
- [ClawHub skill page](https://clawhub.ai/martin2877/skills/tophant-clawvault-mask-project)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration]

**Output Format:** [JSON response with optional sanitized text or saved policy files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns numbered non-reversible placeholders, detection counts, warnings, and optional output file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
