## Description:

Build a URL, get an SVG chart — pie, bar, line, radar, gauge, sankey, QR, any ECharts chart, from x-cmd.com/draw. No install, no key, no stored data. Embed as [![chart]](/draw/explore) — click to explore/edit. The URL is the data — humans see the story, agents get exact numbers. No vision tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwinjhlee](https://clawhub.ai/user/edwinjhlee)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and teams use the skill to create shareable charts for READMEs, issues, reports, and chat. Agents can read the chart data from its URL or SVG metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted chart URLs and SVGs contain the underlying chart data and may be shared with the service and link recipients.

Mitigation: Use hosted links only for data that can be shared; render confidential charts locally with a reviewed renderer.

Risk: The optional CLI fallback downloads a package on initial use.

Mitigation: Pin a reviewed package version before using the CLI fallback.

## Reference(s):

- [x-cmd Draw documentation](https://x-cmd.com/draw)

## Skill Output:

**Output Type(s):** [URLs, SVG charts, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with chart URLs and shell command examples; chart outputs are SVG or PNG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart URLs encode the data and settings; SVG metadata also contains the chart data. Local CLI commands can save SVG or PNG files.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
