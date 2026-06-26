## Description: <br>
Fetches Ptengine heatmap data through ptengine-cli and produces CRO behavior analysis reports using a four-stage psychology model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaichen](https://clawhub.ai/user/zhaichen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing practitioners, CRO specialists, site operators, and developers use this skill to analyze Ptengine heatmap data for a page, compare visitor segments, validate A/B tests, evaluate ad channels, and identify conversion barriers or opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local Ptengine credentials and may expose sensitive analytics data if prompts, logs, or reports are shared carelessly. <br>
Mitigation: Configure the Ptengine API key with appropriate permissions and avoid sharing credentials, logs, prompts, or generated reports that contain sensitive analytics data. <br>
Risk: The skill installs and runs ptengine-cli locally before analysis can proceed. <br>
Mitigation: Use the bundled install.sh wrapper, which downloads a pinned installer and verifies its checksum before execution. <br>
Risk: Heatmap analysis can be misleading if it mixes historical Ptengine data with live page scraping or screenshots from another source. <br>
Mitigation: Use only ptengine-cli output as the authoritative source, and ask the user for missing block content rather than fetching the page through other tools. <br>


## Reference(s): <br>
- [Ptengine CLI Command Reference](references/ptengine-cli.md) <br>
- [Data Transformation Reference](references/data-transform.md) <br>
- [Quality Constraints](references/quality-constraints.md) <br>
- [Page Classification](references/page-classification.md) <br>
- [Page Type Interpretation Guide](references/page-types.md) <br>
- [Single Page Analysis](references/single-page-task.md) <br>
- [Compare Cross-Segment Analysis](references/compare-task.md) <br>
- [A/B Test Hypothesis Validation](references/ab-test-task.md) <br>
- [Ad Performance Analysis](references/ad-performance.md) <br>
- [Audience Analysis](references/audience-analysis.md) <br>
- [Block Content Analysis and Stage Classification](references/block-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Human-readable Markdown report with setup and data-fetch commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Ptengine CLI responses as the authoritative data source and may require a Ptengine API key and profile ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
