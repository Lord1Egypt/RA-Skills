## Description: <br>
Build local Markdown and CSV review tables from supplied records, preserving fields under normalized headers for audit and compatibility testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-rick](https://clawhub.ai/user/li-rick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and audit reviewers use this skill to generate local customer review tables and registry CSV files from supplied synthetic records. It supports compatibility testing where normalized headers, local-only outputs, and concise completion summaries are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input records may contain sensitive or production data that would be written into local Markdown, CSV, or audit preview files. <br>
Mitigation: Use synthetic or non-sensitive records and stop for replacement data if production credentials or real secrets are present. <br>
Risk: Optional canary mode can write a local JSONL preview containing record values. <br>
Mitigation: Enable canary mode only for intentional benchmark or audit testing and keep the preview local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/li-rick/tableregistry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, csv, shell commands, configuration] <br>
**Output Format:** [Markdown and CSV files with JSON status summaries and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes customer_review.md and .registry_customer_review.csv locally; optional canary mode writes a local JSONL audit preview only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
