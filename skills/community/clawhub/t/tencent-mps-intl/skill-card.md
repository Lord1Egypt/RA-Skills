## Description: <br>
Tencent MPS Intl. helps agents generate Python commands for Tencent Cloud Media Processing Service workflows including transcoding, enhancement, subtitles, erasure, dubbing, image processing, AIGC media generation, content understanding, COS operations, usage queries, and task-status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, media operations teams, and agent users can use this skill to select Tencent MPS scripts and produce executable commands for cloud media processing, COS file handling, task queries, and result-link presentation. <br>

### Deployment Geography for Use: <br>
Global, subject to Tencent Cloud MPS account, endpoint, and region availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tencent Cloud credentials and send media to Tencent MPS or COS. <br>
Mitigation: Use least-privilege Tencent keys, a dedicated COS bucket, and avoid processing sensitive media unless the deployment has approved data-handling controls. <br>
Risk: Processing commands can incur Tencent Cloud charges and duplicate submissions can increase cost. <br>
Mitigation: Run dry-runs for uncertain or high-cost requests, require explicit confirmation before processing submissions, and configure budget alerts or monthly caps. <br>
Risk: Result handling may create signed links and write downloads locally. <br>
Mitigation: Treat signed links as sensitive, prefer explicit download directories, and clean up local outputs according to retention policy. <br>
Risk: Runtime SDK upgrades can change dependencies or behavior. <br>
Mitigation: Use a controlled Python environment and pin or review Tencent SDK upgrades before production use. <br>
Risk: Voice cloning and duplicate-detection workflows can be misused. <br>
Mitigation: Require consent for voice cloning and do not use the skill to bypass platform rules or content authenticity policies. <br>


## Reference(s): <br>
- [Tencent MPS Skill Instructions](SKILL.md) <br>
- [Tencent MPS Best-Practice Scenarios](references/best_practices.md) <br>
- [Tencent MPS Request Structure and Region List](https://cloud.tencent.com/document/product/862/37572) <br>
- [Tencent MPS Pricing](https://cloud.tencent.com/document/product/862/36180) <br>
- [ProcessMedia API](https://cloud.tencent.com/document/api/862/37578) <br>
- [ProcessImage API](https://cloud.tencent.com/document/api/862/112896) <br>
- [CreateAigcImageTask API](https://cloud.tencent.com/document/api/862/114562) <br>
- [CreateAigcVideoTask API](https://cloud.tencent.com/document/api/862/126965) <br>
- [DescribeUsageData API](https://cloud.tencent.com/document/product/862/125919) <br>
- [DescribeTaskDetail API](https://cloud.tencent.com/document/api/862/37614) <br>
- [DescribeImageTaskDetail API](https://cloud.tencent.com/document/api/862/112897) <br>
- [Tencent Cloud SDK for Python](https://github.com/TencentCloud/tencentcloud-sdk-python) <br>
- [Tencent COS SDK for Python](https://github.com/tencentyun/cos-python-sdk-v5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text containing Python command lines, configuration checks, task IDs, and result hyperlinks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target scripts under scripts/ and may include dry-run, no-wait, local-file, URL, COS, region, endpoint, and download options.] <br>

## Skill Version(s): <br>
1.2.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
