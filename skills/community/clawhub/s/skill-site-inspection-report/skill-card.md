## Description:

Generates illustrated HTML site inspection reports from site photos and written inspection notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external inspectors use this skill to collect site inspection observations, confirm a report outline, process inspection photos, and produce a structured internal HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may contain unsanitized report text and should be treated as active content.

Mitigation: Use trusted inspection inputs, review generated report fields before distribution, and sanitize or escape report text where required.

Risk: Inspection photos and report data are written locally and embedded into a distributable HTML file.

Mitigation: Store generated files only in approved locations and remove local artifacts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-site-inspection-report)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-site-inspection-report)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Report template](assets/report-template.html)
- [Image processing script](scripts/process_images.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance, Markdown report outline, shell command, JSON image data, and generated HTML report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local HTML report and local image_data.json after processing supplied inspection images.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
