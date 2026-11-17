## Description:

This skill helps agents generate Russian glucose monitoring device market research reports from supplied or SerpAPI-collected data, with Markdown and Word document outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External business and market intelligence users can use this skill to assemble a Russian blood glucose meter and test strip market report covering market size, competitors, e-commerce pricing, policy signals, medical research, tenders, and entry recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure local API credentials.

Mitigation: Use environment variables or an untracked local configuration file instead of storing credentials in packaged files.

Risk: The skill requires installing dependencies and running local Python scripts.

Mitigation: Review the code first, install dependencies in a virtual environment or container, and avoid privileged package installation.

Risk: The advertised real-time search behavior may be incomplete in the packaged implementation.

Mitigation: Validate generated reports against trusted source data before relying on them for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxuan1992asia-svg/skills/xuanself-realtime)
- [SerpAPI](https://serpapi.com)
- [IDF Diabetes Atlas](https://diabetesatlas.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Word documents, JSON inputs, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use SerpAPI credentials and local Python dependencies; can generate Markdown and .docx report files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files declare 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
