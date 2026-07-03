## Description: <br>
面向现代农业的AI智能体技能，支持作物生长监测、病虫害识别与防治、气候风险分析、农事作业规划、农产品市场价格追踪、土壤分析与肥料推荐。服务种植户、农业企业和农技人员。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Growers, agricultural enterprises, and agricultural technical staff use this skill for crop monitoring, pest and disease triage, climate-risk review, farm-work planning, and market-timing support. <br>

### Deployment Geography for Use: <br>
Global; the artifact describes the supporting crop and pest data as focused on major Chinese crop varieties and common pests. <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release suspicious due to possible full local access, approval-bypass execution, and external diff sharing in a bundled helper. <br>
Mitigation: Review the installed files before use; avoid approval-bypass execution and disable external diff-sharing review tools unless those permissions are intentionally approved. <br>
Risk: Crop and pest analysis can be wrong when image quality is poor or the case is outside the covered crop and pest data. <br>
Mitigation: Use clear multi-angle photos, treat results as decision support, and verify important diagnoses with qualified agricultural expertise. <br>
Risk: Weather, climate, and market guidance may be stale or incomplete for urgent operational decisions. <br>
Mitigation: Check current trusted weather alerts, market sources, and local conditions before scheduling field operations or sales. <br>
Risk: Pesticide and treatment recommendations may be subject to local law, label restrictions, and safety intervals. <br>
Mitigation: Follow local regulations, product labels, and required safety intervals before applying any treatment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/smart-agriculture) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown reports and structured recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include crop diagnosis, climate briefings, farm calendars, market summaries, and safety reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
