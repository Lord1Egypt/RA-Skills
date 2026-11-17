## Description: <br>
Supports basic single-source report configuration with field mapping, sum, count, and average aggregation, filtering, sorting, and Markdown, JSON, or CSV export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and small teams use this skill to turn a single CSV, JSON, or Markdown table into a summarized report with basic filtering, sorting, aggregation, and export options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests shell execution for a basic reporting workflow. <br>
Mitigation: Remove shell execution where possible, or tightly limit it to reviewed commands in a constrained workspace. <br>
Risk: Remote data behavior is under-scoped for reports that may contain sensitive data. <br>
Mitigation: Treat remote data access as disabled unless explicitly intended and reviewed for what data may leave the local environment. <br>
Risk: Sensitive report inputs or exports may expose business data if used without review. <br>
Mitigation: Review the skill before installing it for sensitive reports and verify output paths and exported content before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/report-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, files, guidance] <br>
**Output Format:** [Markdown, JSON, or CSV report output with a JSON-style result envelope and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report path, row count, columns, aggregation, grouping, preview, source metadata, generation timestamp, and duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
