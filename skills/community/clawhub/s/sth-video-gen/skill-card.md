## Description: <br>
Generates vertical 9:16 videos for Sing The Hook song templates through a two-stage MCP video pipeline with trimming, GCS upload, and database updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuyinzhuyin](https://clawhub.ai/user/zhuyinzhuyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing Sing The Hook song templates use this skill to process CSV batches, generate lip-synced vertical videos from template images, prompts, and audio mixes, and write resulting video URLs back to the target database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can persistently update PostgreSQL song template records and CSV status fields. <br>
Mitigation: Run it only against an intended test or least-privileged database, and review the CSV input before execution. <br>
Risk: The workflow sends prompts and media URLs to an external MCP video-processing endpoint and downloads returned media. <br>
Mitigation: Use only approved media URLs and MCP credentials, restrict outbound network access where possible, and verify generated URLs before upload or database update. <br>
Risk: The workflow uploads trimmed videos to GCS using a service-account key. <br>
Mitigation: Use a least-privileged service account scoped to the intended bucket and rotate or remove credentials after batch work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuyinzhuyin/sth-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zhuyinzhuyin) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [fetch_asset_examples.md](artifact/fetch_asset_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown instructions with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the bundled scripts can update CSV rows, local JSON state, log files, GCS video files, and PostgreSQL video URL/status fields.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
