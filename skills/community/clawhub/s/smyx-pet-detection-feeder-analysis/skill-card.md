## Description: <br>
Uses computer vision to detect and recognize cats and dogs in smart-feeder or IPC camera media, including pet identity matching, enrollment, and history-report lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze smart-feeder or IPC camera images, videos, or media URLs for pet detection, cat/dog classification, pet identity recognition, pet enrollment, and cloud history-report retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media files, media URLs, and pet-analysis history queries may be sent to Lifeemergence/Open API services and associated with an automatically selected local identity. <br>
Mitigation: Use only media and URLs that are appropriate to share with that backend, and avoid private camera URLs unless its retention and access practices are acceptable. <br>
Risk: The skill silently creates or reuses a local user identity and may store tokens in the local workspace data directory or SQLite database. <br>
Mitigation: Review and protect the local workspace data directory, and remove or rotate stored credentials when the skill is no longer needed. <br>
Risk: Pet recognition results and feeding suggestions can be incorrect or incomplete. <br>
Mitigation: Treat outputs as advisory and confirm important feeding, identity, or health-related decisions manually. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-detection-feeder-analysis) <br>
- [API Reference](references/api_doc.md) <br>
- [Shared Analysis API Reference](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports and tables with optional JSON result blocks and file output paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links and pet detection, enrollment, or history-query results derived from remote API responses.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter states 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
