## Description:

Provides local cross-document similarity analysis for tender files with paragraph-level duplicate detection and visual HTML reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliwenjing](https://clawhub.ai/user/wuliwenjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and proposal teams use this skill to compare local tender documents, identify duplicate or highly similar paragraphs, and produce a reviewable similarity report without uploading source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may contain sensitive tender content.

Mitigation: Store and share reports as sensitive documents, and avoid opening reports from untrusted inputs in a browser with network access.

Risk: The dependency helper and runtime controls require review before installation.

Mitigation: Install only reviewed dependencies in an isolated Python environment, preferably from pinned versions.

Risk: Network-isolation behavior can affect the current Python process.

Mitigation: Run the analyzer in a short-lived subprocess or container so isolation changes do not disrupt other tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuliwenjing/skills/tender-similarity-analyzer)
- [ClawHub publisher profile](https://clawhub.ai/user/wuliwenjing)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Console text plus an HTML similarity report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes at least two local DOCX, PDF, TXT, or Markdown files and can write the report to a user-specified path.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact version history lists v2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
