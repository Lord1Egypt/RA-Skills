## Description:

Triggers when a user provides a video URL or file of a pet (cat/dog/bird) for analysis; supports local video uploads or network URLs to call server-side APIs for health checks, analyzing features like fur, body, and face to identify potential diseases and generate a Pet Safety Guardian health report. | 猫狗宠物健康诊断分析工具，当用户提供猫/狗/鸟等宠物的视频 URL 或文件需要分析时，触发本技能进行宠物健康诊断分析；支持通过上传本地视频或网络视频 URL，调用服务端 API 进行宠物健康检查，分析毛发、身体、脸部等特征，识别潜在疾病并输出宠安卫士健康报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and caregivers can submit a cat, dog, bird, or other pet video for an automated health screening, structured report, and care suggestions, or request their cloud report history. The analysis is informational and does not replace a veterinarian's diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because scanners report possible disclosure of video and credentials.

Mitigation: Avoid providing credentials or sensitive footage until reviewed, and submit video only when comfortable with the service receiving it.

Risk: ClawScan reports unsafe request behavior and extra identity or history operations.

Mitigation: Check that the intended service destination is honored and review the account and report-history behavior before use.

## Reference(s):

- [Skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown, Guidance]

**Output Format:** [Structured pet health report with analysis text and a report link; historical reports can be returned as JSON and formatted in a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observations, potential health concerns, care suggestions, and report links; informational only and not a veterinary diagnosis]

## Skill Version(s):

999.999.1015 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
