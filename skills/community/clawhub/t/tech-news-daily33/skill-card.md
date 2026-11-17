## Description:

Generates daily technology news HTML reports from IT Home and MyDrivers/Kuai Technology with full text, images, and categorized sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choksta](https://clawhub.ai/user/choksta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to collect public Chinese technology news inputs and generate a styled daily HTML report with categorized articles and embedded local images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled generator uses hard-coded local input, image, and output paths.

Mitigation: Patch the script to accept user-configurable paths through arguments, environment variables, or a checked configuration file before running it.

Risk: Unsafe local file and link handling may expose users to unexpected files or non-web links from untrusted JSON input.

Mitigation: Validate the JSON schema, constrain image keys to safe filenames, and allow only http or https article URLs before generating the report.

## Reference(s):

- [Data format reference](artifact/references/data_format.md)
- [Skill page](https://clawhub.ai/choksta/skills/tech-news-daily33)
- [IT Home RSS source](https://www.ithome.com/rss/)
- [MyDrivers news source](https://news.mydrivers.com/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, HTML files]

**Output Format:** [Markdown guidance with a Python script and generated HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expects a six-field JSON news array and a local image directory; generated reports embed matching local images as base64 data URIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
