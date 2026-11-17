## Description:

Generates HTML technical R&D briefs from patent Excel workbooks by tagging relevant patents, analyzing trends, and assembling report sections for industry news, companies, technology categories, and patent details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to generate patent-focused technical report files from Excel exports for a specified technology topic and date range. The agent collects inputs, checks topic configuration, runs the reporting scripts, and reports the generated file paths and summary counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable topic configuration files can run arbitrary Python when loaded.

Mitigation: Review all *_keywords.py and *_content.py files before use and run the skill only with trusted publisher-provided or locally authored configuration.

Risk: The workflow may install Python dependencies automatically.

Mitigation: Run the skill in an isolated Python environment and install dependencies from reviewed requirements before processing workbooks.

Risk: The report generator fetches a decorative background image from the network.

Mitigation: Disable or remove network image download for sensitive, restricted, or offline work.

Risk: Generated HTML may include workbook-derived text and links without complete escaping or URL validation.

Mitigation: Process only trusted Excel workbooks and avoid opening or sharing generated reports from untrusted workbooks until HTML escaping and URL validation are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/tech-report-skill)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [Patsnap analytics](https://analytics.zhihuiya.com/)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [Sample data requirements](artifact/examples/SAMPLE_DATA.md)
- [Implementation improvements](artifact/IMPROVEMENTS.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated Excel and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved beside the input workbook and may include embedded patent images, hyperlinks, and topic-specific content loaded from Python configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is v1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
