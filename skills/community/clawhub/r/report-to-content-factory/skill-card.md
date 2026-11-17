## Description:

Turns industry-report evidence into original WeChat articles, Xiaohongshu posts, and spoken-video scripts with citations and visual suggestions, retaining sources and drafts in JishuDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to turn research reports or topics into complete, evidence-backed drafts for WeChat, Xiaohongshu, and short videos. It requires an authorized JishuDB connection to retain evidence and revisions; it does not publish content or produce finished videos or covers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install JishuDB Desktop and modify local client configuration.

Mitigation: Review the concrete installation plan and approve it before setup; decline if local installation or configuration changes are unwanted.

Risk: Source material, brand preferences, and draft revisions are retained in JishuDB.

Mitigation: Confirm the intended destination and retention scope, and authorize the research and writes before storing material.

Risk: Report-based content could misstate evidence or reuse restricted material.

Mitigation: Check claims against inspected sources, keep citations and coverage limits, and respect source access and reuse rights.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bowen-aijishu/skills/report-to-content-factory)
- [Skill homepage declared in release metadata (not verified import provenance)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/report-to-content-factory)
- [Report discovery and evidence contract](references/evidence-contract.md)
- [JishuDB setup quickstart](references/jishudb-setup/references/setup-quickstart.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown drafts, citations, and visual suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requested formats only; source evidence and draft revisions retained in JishuDB.]

## Skill Version(s):

0.1.17 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
