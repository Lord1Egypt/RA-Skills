## Description: <br>
一键生成结构化周报、月报及项目报告，并可按飞书云文档格式输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, teams, and external developers use this skill to turn work notes, recent conversation context, or project updates into structured weekly reports, monthly reports, project reports, and meeting minutes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include sensitive chat history or work context. <br>
Mitigation: Use only on explicit user request and review generated report content before sharing or publishing. <br>
Risk: Feishu-style document output may expose content to an unintended workspace or recipients. <br>
Mitigation: Verify document destination, permissions, and recipients before relying on Feishu document creation or sharing. <br>
Risk: The artifact may claim document creation even when a real integration is not confirmed. <br>
Mitigation: Confirm that any Feishu integration creates an actual document in the intended workspace before treating the returned document reference as authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/zhoubao-yuebao) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact metadata](artifact/metadata.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown-style structured report text with optional Feishu document reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated sections for completed work, metrics, next plans, risks, and blockers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
