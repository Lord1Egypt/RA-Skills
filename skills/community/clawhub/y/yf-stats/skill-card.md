## Description:

Fetches stock data and generates price charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grayson85](https://clawhub.ai/user/grayson85)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Yahoo Finance ticker data and optionally generate a six-month price chart for a requested symbol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled ticker and chart flag values may be passed through the command template unsafely.

Mitigation: Validate ticker symbols, restrict chart flag values to the documented option, and pass arguments without shell interpolation.

Risk: Chart generation writes an output file based on the requested ticker symbol.

Mitigation: Write generated charts only to a dedicated safe directory after ticker validation.

Risk: Runtime dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before broad or sensitive use.

## Reference(s):

- [yf-stats ClawHub skill page](https://clawhub.ai/grayson85/skills/yf-stats)

## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [Console text with optional PNG chart file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When chart output is requested, the artifact behavior writes a ticker-named PNG chart in the working directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
