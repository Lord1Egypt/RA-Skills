## Description:

Extracts website assets and page content, including images, SVGs, fonts, videos, page structure, and asset catalogs, across one or more URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorukardahan](https://clawhub.ai/user/dorukardahan)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect supplied websites, collect web assets, save extracted page metadata, and produce a final extraction manifest for design or implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to browse supplied websites and may encounter untrusted or attacker-controlled pages.

Mitigation: Use it in a restricted workspace and network environment, and avoid untrusted sites until URL validation and allowlists are added.

Risk: The skill downloads remote assets and writes files into the local project.

Mitigation: Review target URLs and output paths before execution, and inspect generated files before using them in a project.

Risk: The skill spawns background extraction tasks, which can make activity harder to monitor.

Mitigation: Require explicit confirmation for multi-site runs and review each background task's final report and failed-download list.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline bash, JavaScript snippets, JSON manifests, and downloaded asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local asset directories, page-content JSON, asset URL catalogs, and an asset-manifest.json summary.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
