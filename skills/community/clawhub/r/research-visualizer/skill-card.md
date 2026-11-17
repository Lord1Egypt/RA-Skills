## Description:

Generate interactive HTML research reports from AI research context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frrrrrrrrank](https://clawhub.ai/user/frrrrrrrrank)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill after multi-step research to turn searches, API calls, analysis steps, sources, visualizations, and conclusions into an interactive report link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research summaries, source metadata, and conclusions may be published as durable hosted HTML links.

Mitigation: Use the skill only for information suitable for hosted sharing, or disable/review upload behavior before using it with confidential, regulated, private, or internal investigations.

Risk: The server security summary flags unsafe upload and report-rendering code that needs review before trusted use.

Mitigation: Review and fix the upload/report-rendering implementation before deployment in trusted environments.

Risk: Public report generation with no encryption can expose sensitive content.

Mitigation: Do not use the public no-encryption mode for sensitive reports.

## Reference(s):

- [Openclaw Research Viz on ClawHub](https://clawhub.ai/frrrrrrrrank/skills/research-visualizer)
- [Publisher profile](https://clawhub.ai/user/frrrrrrrrank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown link card with generated HTML report URLs and optional local file URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates self-contained HTML research reports from structured JSON research context; hosted reports may be encrypted unless public output is explicitly requested.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
