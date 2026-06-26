## Description: <br>
Generates commands and configuration guidance for Tencent Cloud MPS video dubbing workflows that translate video language, burn translated subtitles, clone voice dubbing, and query task results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and video localization operators use this skill to prepare and run Tencent Cloud MPS end-to-end dubbing tasks for producing a new language version of a video and checking task status. <br>

### Deployment Geography for Use: <br>
Tencent Cloud MPS supported API regions listed by the skill: ap-guangzhou, ap-shanghai, ap-beijing, ap-hongkong, ap-singapore, ap-chengdu, ap-chongqing, ap-jakarta, ap-bangkok, ap-seoul, ap-tokyo, na-ashburn, na-siliconvalley, sa-saopaulo, eu-frankfurt. <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos may be uploaded to Tencent Cloud COS or processed by Tencent Cloud MPS, including local-file inputs used during previews. <br>
Mitigation: Use only approved media, avoid local-file dry runs unless upload is acceptable, and use dedicated least-privilege Tencent credentials for this skill. <br>
Risk: Processing commands can incur Tencent Cloud MPS fees, and repeated submissions before a task result is available can duplicate charges. <br>
Mitigation: Require explicit charge confirmation for processing commands, use dry runs or task queries for previews and status checks, and track the TaskId before resubmitting. <br>


## Reference(s): <br>
- [Video Dubbing Parameters and Examples](references/mps_video_dubbing.md) <br>
- [ProcessMedia Request Examples](references/example.md) <br>
- [Tencent Cloud MPS ProcessMedia AiAnalysisTask](https://cloud.tencent.com/document/product/862/37578) <br>
- [Tencent Cloud MPS One-Stop Dubbing Access](https://cloud.tencent.com/document/product/862/124504) <br>
- [Tencent Cloud MPS DescribeTaskDetail](https://cloud.tencent.com/document/api/862/37614) <br>
- [Tencent Cloud MPS Region List](https://cloud.tencent.com/document/product/862/37572) <br>
- [Tencent Cloud MPS Pricing](https://cloud.tencent.com/document/product/862/36180) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell commands and Markdown result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may submit Tencent Cloud MPS tasks, poll for completion, download outputs, list languages, query task status, or check environment configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
