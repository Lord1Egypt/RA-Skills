## Description: <br>
AI-powered orchid growth-status detection from orchid images or videos, including visible roots in transparent pots, that reports shoot count, flower-spike growth, root condition, overall vitality, and care guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as orchid hobbyists, greenhouse operators, and horticulture studios use this skill to analyze orchid media for new shoots, flower spikes, root color, root health, and plant vitality. It can also return cloud-stored historical report records for the internally associated user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads orchid images or videos to a cloud-backed analysis service and can query cloud report history. <br>
Mitigation: Use it only with media suitable for remote processing and deploy it where cloud report access is acceptable. <br>
Risk: The skill silently creates or reuses an internal identity and persists local account tokens. <br>
Mitigation: Run it in isolated workspaces or accounts, and clear local state before switching users or sharing an environment. <br>
Risk: Historical report access is tied to the internally associated identity. <br>
Mitigation: Confirm identity and report isolation requirements before enabling history queries in shared or multi-user deployments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-orchid-growth-status-detection-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [Orchid Analysis API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON analysis details, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports image/video files or URLs, cloud-backed report retrieval, and optional output-file writing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
