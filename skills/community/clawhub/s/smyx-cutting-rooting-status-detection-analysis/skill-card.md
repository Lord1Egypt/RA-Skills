## Description: <br>
Analyzes plant-cutting images or videos captured through transparent containers to identify root primordia, classify rooting stage, and return monitoring guidance with report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to submit plant-cutting media from transparent propagation containers for non-invasive rooting progress assessment. It can also query cloud-hosted report history and return structured results, report links, and transplant-timing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends plant images, videos, or supplied media URLs to Life Emergence cloud services for analysis. <br>
Mitigation: Use only media that is appropriate for external cloud processing; avoid private camera feeds, internal URLs, sensitive research media, or confidential facility imagery. <br>
Risk: The skill silently creates or reuses an account identity and stores service tokens in the local workspace for report history access. <br>
Mitigation: Install only in workspaces where silent account persistence is acceptable, and isolate or clear the workspace when shared use or token retention is not desired. <br>
Risk: The skill can query cloud-hosted analysis history associated with the internally resolved identity. <br>
Mitigation: Review who can access the workspace and skill execution context before enabling report-history queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-cutting-rooting-status-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or structured JSON text with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rooting-stage classifications, root-point counts or distribution notes, transplant-timing guidance, cloud report history, and exported report URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
