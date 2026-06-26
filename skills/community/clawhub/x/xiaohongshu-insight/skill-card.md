## Description: <br>
Xiaohongshu viral content data insight tool for querying viral posts, analyzing category trends, and exporting engagement data for content planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and content analysts use this skill to inspect Xiaohongshu viral-post examples, trend summaries, and exportable engagement datasets for creative reference and competitor research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill presents itself as a live Xiaohongshu trend data service while included scripts generate mock data. <br>
Mitigation: Treat reports, viral-post lists, and competitor analysis as demonstration outputs unless the publisher documents a live data source and update mechanism. <br>
Risk: Export commands write CSV, JSON, or XLSX files to caller-provided paths. <br>
Mitigation: Review output filenames and paths before running exports, especially in shared workspaces. <br>


## Reference(s): <br>
- [Data Schema](references/data_schema.md) <br>
- [Viral Criteria](references/viral_criteria.md) <br>
- [ClawHub Release Page](https://clawhub.ai/openlark/xiaohongshu-insight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON records, CSV files, XLSX files, and terminal tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports are written to user-selected output paths; query and trend scripts can print results to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
