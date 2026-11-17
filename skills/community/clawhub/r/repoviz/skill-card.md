## Description:

Scans codebases or supplied logic and creates architecture, flow, data-flow, sequence, and related diagrams as shareable URLs, with optional SVG, PNG, or HTML export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiakai](https://clawhub.ai/user/qiakai)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use repoviz to map repository architecture, trace flows, and document system design with shareable diagrams. They can request local SVG, PNG, or HTML exports when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram labels are sent to the external renderer in URLs and may appear in server access logs.

Mitigation: Keep secrets, credentials, and confidential system names out of diagram labels.

Risk: The explicit short-link option uploads the chart definition for permanent public storage.

Mitigation: Use short links only for chart definitions intended to be public.

## Reference(s):

- [Architecture diagrams](references/architecture.md)
- [Flowcharts and sequence diagrams](references/flowchart.md)
- [Sankey diagrams](references/sankey.md)
- [Chart types and general charts](references/general-charts.md)
- [Repository IR and evidence protocol](references/repository-ir.md)
- [x-cmd Draw documentation](https://x-cmd.com/draw)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Markdown with shareable diagram URLs and notes; optional SVG, PNG, or standalone HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The default response writes no local files; local exports require an explicit request.]

## Skill Version(s):

0.3.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
