## Description:

Automatically parses PDF and text research reports to extract key viewpoints, data, investment advice, risks, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangq0687](https://clawhub.ai/user/zhangq0687)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to process individual or batches of financial research reports, extracting structured highlights, risk warnings, investment advice, and summaries into a local knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive reports are processed through a local Ollama setup and extracted results are stored persistently on disk.

Mitigation: Process only reports approved for the local environment, restrict access to the output directory, and remove stored JSON results when retention is not needed.

Risk: Generated investment advice, extracted figures, and summaries may be incomplete or inaccurate.

Mitigation: Require human review before using extracted data or advice for financial, business, or compliance decisions.

Risk: Reports from untrusted sources may contain misleading content or malformed files that affect extraction quality.

Mitigation: Prefer trusted report sources and validate extracted results against the original document before sharing or acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime report-processing results are saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Ollama model and PDF text extraction tooling; stores processed report outputs under ~/.openclaw/workspace/data/reports/.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
