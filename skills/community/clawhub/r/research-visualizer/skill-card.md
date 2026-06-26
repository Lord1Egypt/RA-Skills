## Description: <br>
Generate interactive HTML research reports from AI research context after multi-step research, including the research process, data visualizations, and conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frrrrrrrrank](https://clawhub.ai/user/frrrrrrrrank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill after multi-step research to turn research steps, source links, data visualizations, and conclusions into an interactive HTML report and shareable link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research summaries, source URLs, and process details can be packaged and uploaded to remote infrastructure. <br>
Mitigation: Install only when those details are acceptable to upload, avoid confidential or regulated research, and review each generated report before sharing. <br>
Risk: Using public report output can expose the full report HTML. <br>
Mitigation: Keep encryption enabled and do not use --no-encrypt unless the report is intended to be public. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frrrrrrrrank/research-visualizer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown link card plus generated interactive HTML report from structured JSON research context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Reports may be encrypted by default and can be uploaded to remote hosting or saved locally when upload fails.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
