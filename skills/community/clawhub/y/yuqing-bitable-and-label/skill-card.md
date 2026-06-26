## Description: <br>
Incrementally syncs XiaoAi public-opinion data into Feishu Bitable and can optionally label records with machine-generated type, sentiment, competitor, device, brand-safety, and content-safety annotations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FrankieWay](https://clawhub.ai/user/FrankieWay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to move XiaoAi monitoring records into a Feishu Bitable workspace and enrich those records for public-opinion triage. It is intended for workflows that can provide Feishu app credentials, XiaoAi access, and a target Bitable URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Feishu app secrets, XiaoAi tokens, cached access tokens, and optional model-gateway credentials. <br>
Mitigation: Use least-privilege credentials, keep .env and .cache private, and avoid setting model-gateway credentials unless record contents are allowed to leave the Feishu and XiaoAi environment. <br>
Risk: The skill writes and updates records in the target Feishu Bitable and may create additional table data during synchronization. <br>
Mitigation: Run against a scoped Bitable view or test workspace first, and grant only the Feishu permissions needed for the intended table. <br>
Risk: The default XiaoAi base URL in the artifact uses HTTP, which can expose traffic or tokens on untrusted networks. <br>
Mitigation: Prefer an HTTPS XiaoAi base URL when the service supports it. <br>
Risk: Included shell scripts perform local maintenance such as cache cleanup, lock-file handling, log rotation, and status updates. <br>
Mitigation: Review shell scripts before scheduled execution and avoid running them on untrusted files or shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FrankieWay/yuqing-bitable-and-label) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Enhanced usage notes](artifact/README_ENHANCED.md) <br>
- [Labeling skill definition](artifact/LABEL_SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Feishu Bitable records, Status counts] <br>
**Output Format:** [Console text with inserted_count and labeling_updated_count fields, plus writes to Feishu Bitable records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, XiaoAi API access, and a target Bitable URL; optional labeling may call an OpenAI-compatible model gateway when configured.] <br>

## Skill Version(s): <br>
2.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
