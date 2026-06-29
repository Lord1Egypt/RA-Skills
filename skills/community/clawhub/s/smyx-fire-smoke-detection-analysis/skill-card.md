## Description: <br>
Detects fire and smoke in video scenes, supporting video stream and image analysis for early warning scenarios such as security surveillance, forest fire prevention, and industrial parks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze surveillance videos, image files, or public media URLs for flame and smoke indicators, then receive structured detection results, recommendations, report links, or historical cloud report listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media files and URLs are processed by an external cloud service, which can expose sensitive surveillance footage or internal-only URLs. <br>
Mitigation: Use only media and URLs acceptable for external cloud processing, and confirm the provider's retention, access control, and data handling expectations before deployment. <br>
Risk: The skill can silently create or reuse an identity, store service tokens locally, and retrieve cloud report history with limited user control. <br>
Mitigation: Review local workspace data storage, token handling, and cloud history access before installation; avoid shared workspaces unless identity and token lifecycle controls are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-fire-smoke-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API reference](references/api_doc.md) <br>
- [Shared analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown summaries and JSON-formatted structured analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detection status, risk information, recommendations, report links, saved output files, or historical report tables.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
