## Description:

Generates structured technical reports in Markdown by collecting report inputs and applying a style guide to a predefined template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dapan0902](https://clawhub.ai/user/dapan0902)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and business users can use this skill to draft structured technical reports, summaries, and analysis documents for technical, executive, or general audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad report, summary, or analysis requests.

Mitigation: Confirm the user's intended report topic, audience, and required findings before drafting the final Markdown report.

Risk: Referenced file paths and frontmatter formatting appear inconsistent in the packaged artifact.

Mitigation: Verify that the style guide and report template can be resolved in the target agent environment before release.

Risk: Generated reports may include incomplete or misleading analysis if the user provides sparse inputs.

Mitigation: Ask for missing topic, key findings, data points, and target audience before completing the report.

## Reference(s):

- [Technical Report Style Guide](artifact/references/references:style-guide.md)
- [Report Template](artifact/assets/assets:report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown technical report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the template sections for executive summary, introduction, key findings, detailed analysis, recommendations, conclusion, and generated date.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
