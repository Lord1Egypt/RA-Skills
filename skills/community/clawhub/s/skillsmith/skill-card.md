## Description:

Scaffold a new OpenClaw skill project with starter docs, tests, fixtures, and optional security workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Skillsmith to create a reviewable starting structure for OpenClaw skill projects, including starter instructions, docs, tests, fixtures, and optional security workflow files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using `--force` can replace an existing target project directory.

Mitigation: Run without `--force` by default, choose a dedicated output directory, and inspect the target path before allowing replacement.

Risk: The optional generated CI workflow runs an unpinned scanner package.

Mitigation: Review the workflow before committing it and pin scanner versions or approved package sources according to the repository policy.

Risk: Generated scaffold files are placeholders rather than complete production logic.

Mitigation: Replace placeholder instructions, scripts, tests, and policy files with project-specific content before release or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike007jd/skills/skillsmith)
- [ClawHub publisher profile](https://clawhub.ai/user/mike007jd)

## Skill Output:

**Output Type(s):** [files, markdown, code, shell commands, configuration]

**Output Format:** [Project files with Markdown documentation, JavaScript code, JSON configuration, and optional YAML workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated project contents depend on CLI flags such as template, CI inclusion, prompts, output directory, and force overwrite.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
