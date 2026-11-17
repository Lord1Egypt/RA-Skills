## Description:

Generate and sync a README environment-variable table from .env.example using marker blocks, with drift detection for CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to keep README environment-variable documentation aligned with a project's env template and to detect documentation drift in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apply mode rewrites the selected README marker block.

Mitigation: Run the default report mode first and review generated README diffs before committing changes.

Risk: Generated Markdown table content may reflect values from the selected env template.

Mitigation: Keep ENV_FILE and README_FILE scoped to trusted project files, especially when env templates can be changed by untrusted contributors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/readme-env-table-sync)
- [ClawHub publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown table updates and short command-line summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses report mode for drift detection and apply mode to rewrite the selected README marker block.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
