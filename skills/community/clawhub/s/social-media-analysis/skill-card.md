## Description: <br>
Analyzes social media records from Feishu Bitable views by checking URLs, downloading media, extracting video frames, and generating concise content summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankieway](https://clawhub.ai/user/frankieway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to backfill social-media analysis fields in Feishu Bitable records, including link validity, media type, downloaded media evidence, and short content summaries for supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Feishu application credentials and can update Feishu Bitable records. <br>
Mitigation: Use a dedicated low-privilege Feishu app, start with a non-sensitive test table, and review permissions before running against production records. <br>
Risk: The skill performs broad social-platform scraping, media downloads, and local writes. <br>
Mitigation: Restrict table URLs to expected platforms and run downloads in an isolated workspace with quotas and cleanup. <br>
Risk: Some Xiaohongshu workflows may require session cookies. <br>
Mitigation: Avoid personal cookies where possible and never paste cookies into shared terminals, logs, or persisted command histories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankieway/social-media-analysis) <br>
- [WORKFLOW_V2.md](WORKFLOW_V2.md) <br>
- [scripts/README.md](scripts/README.md) <br>
- [scripts/QUICKSTART.md](scripts/QUICKSTART.md) <br>
- [Feishu Bitable API documentation](https://open.feishu.cn/document/ukTMukTMukTM/uADO1UjLwgjB14CN) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download media files, write local artifacts, and update Feishu Bitable records; generated content summaries are capped at 100 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
