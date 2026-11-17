## Description:

OpenClaw YouTube Publisher is a public ClawHub YouTube publishing skill. Use it when the user says "youtube creator ops", "youtube publisher", "YouTube Studio publish", or wants to publish a YouTube Short through a logged-in browser profile with a reusable run report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to publish YouTube Shorts through a logged-in OpenClaw browser session while keeping a reusable manifest, source-provenance record, publish log, bundle check, and markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill acts through a logged-in YouTube browser profile and can prepare a real publish flow.

Mitigation: Use only a browser profile intentionally selected for this workflow, keep the run in dry_run until explicit publish approval, and treat the final publish action as user-approved.

Risk: Generated manifests, step notes, or reports may include private URLs, local paths, browser-profile labels, or credentials if the operator records them.

Mitigation: Inspect generated markdown before sharing, avoid placing sensitive values in manifests or notes, rely on the bundled redaction checks, and revoke any credential that appears in a generated report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/youtube-creator-ops)
- [GitHub Homepage](https://github.com/zack-dev-cm/youtube-creator-ops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON manifests, markdown reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports redact browser profile labels, private artifact paths, non-public URLs, and secret-like values before sharing.]

## Skill Version(s):

1.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
