## Description: <br>
Tencent MPS helps agents generate Python commands for Tencent Cloud Media Processing and COS workflows, including transcoding, enhancement, subtitles, image processing, AIGC generation, content understanding, task lookup, usage queries, and comparison pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollielin](https://clawhub.ai/user/ollielin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media operators use this skill to turn Tencent Cloud MPS and COS requests into concrete Python script commands. It is intended for media processing, AI media generation, media analysis, task management, and usage-reporting workflows that may submit cloud jobs and return task IDs or result links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tencent Cloud credentials to upload local media to COS/MPS, create billable processing jobs, generate presigned links, and download results. <br>
Mitigation: Use least-privilege or temporary credentials, confirm commands before execution, prefer dry runs for costly or uncertain tasks, and avoid sensitive files unless cloud processing is approved. <br>
Risk: Duplicate-detection evasion, voice cloning, face swap, and watermark or removal workflows can be misused for impersonation, platform evasion, or unauthorized processing. <br>
Mitigation: Review these workflows before use and restrict them to authorized media, consented identities, and permitted content-processing purposes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ollielin/tencent-mps) <br>
- [Tencent Cloud MPS request regions](https://cloud.tencent.com/document/product/862/37572) <br>
- [Tencent Cloud ProcessMedia API](https://cloud.tencent.com/document/api/862/37578) <br>
- [Tencent Cloud ProcessImage API](https://cloud.tencent.com/document/api/862/112896) <br>
- [Tencent Cloud CreateAigcImageTask API](https://cloud.tencent.com/document/api/862/114562) <br>
- [Tencent Cloud CreateAigcVideoTask API](https://cloud.tencent.com/document/api/862/126965) <br>
- [Tencent MPS best practices](references/best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands, task IDs, and result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target bundled Python scripts and may include dry-run or no-wait flags; processing tasks require explicit confirmation before execution.] <br>

## Skill Version(s): <br>
1.2.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
