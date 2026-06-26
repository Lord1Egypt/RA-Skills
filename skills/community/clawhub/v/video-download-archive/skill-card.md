## Description: <br>
Validate single video URLs, download highest-quality files with yt-dlp, and archive results into a Feishu Bitable using platform tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiernk](https://clawhub.ai/user/feiernk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to process one video URL at a time, download or reconcile a local archive file, and prepare or write metadata records to a configured Feishu Bitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads video files and stores URLs, descriptions, uploader data, and full local file paths in a fixed Feishu Bitable. <br>
Mitigation: Confirm the Feishu app token and table are owned by you or intentionally shared, and review what metadata may be written before running the workflow. <br>
Risk: The runner depends on an unbundled, hard-coded local helper script for downloads. <br>
Mitigation: Inspect, replace, or remove the helper path before installation so the invoked download script is trusted and present on the target system. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review the publisher, security summary, and file behavior before installing or using the skill. <br>


## Reference(s): <br>
- [Video Download Archive release page](https://clawhub.ai/feiernk/video-download-archive) <br>
- [Configured Feishu Bitable target](https://my.feishu.cn/base/KMuEbR5b5aLXFosyxGlc7kTenpb) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the runner plus concise text or Markdown status from the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded video files, .info.json metadata, local file paths, and Feishu Bitable record fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
