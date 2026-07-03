## Description: <br>
Performs AI analysis on input video clips/image content and generates a smooth, natural scene description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to submit clear images, video clips, or media URLs for multimodal visual analysis, scene summarization, and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media files, media URLs, and account-linked analysis data may be sent to lifeemergence.com services. <br>
Mitigation: Review data sensitivity, network policy, and service terms before using the skill with private, regulated, or confidential media. <br>
Risk: The skill may create or reuse a local default identity and retrieve cloud history or report links tied to that identity. <br>
Mitigation: Use the skill only in workspaces where identity reuse is acceptable, and review generated report links before sharing output. <br>
Risk: Authentication tokens may be stored in a workspace SQLite database. <br>
Mitigation: Limit workspace access, rotate credentials if exposure is suspected, and remove local state before handing the workspace to another user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-visual-summary-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Visual summary API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Natural-language scene summaries, structured report text, Markdown tables for history, and optional JSON or file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media paths or public media URLs; documented formats include jpg, jpeg, png, mp4, avi, and mov with a 10 MB limit.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; SKILL.md frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
