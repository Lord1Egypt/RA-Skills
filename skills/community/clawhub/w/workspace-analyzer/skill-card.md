## Description:

Analyzes OpenClaw workspace structure and content to identify maintenance needs, bloat, duplicates, and organization issues, then outputs a JSON report for the agent to review and act upon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zendenho7](https://clawhub.ai/user/zendenho7)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to scan OpenClaw workspaces for structure, bloat, duplicate content, orphaned files, broken wiki links, and single-source-of-truth issues. The resulting JSON report helps an agent or reviewer prioritize manual maintenance work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher writes reports to a fixed /tmp/workspace-analysis.json path, which can expose or overwrite local report data on shared systems.

Mitigation: Run analyzer.py directly with --output set to a private path, or inspect and remove the temp report after use.

Risk: The read-only description understates that report files may be written when an output path is used.

Mitigation: Treat generated reports as local artifacts, choose output destinations deliberately, and review report contents before sharing them.

Risk: Recommendations can guide file edits or commits that change workspace behavior.

Mitigation: Use recommendations as review input only, and manually inspect cleanup, duplicate-content, and commit actions before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zendenho7/skills/workspace-analyzer)

## Skill Output:

**Output Type(s):** [json, guidance, text]

**Output Format:** [JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scan metadata, detected core files, per-file analysis, single-source validation results, recommendations, and summary counts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
