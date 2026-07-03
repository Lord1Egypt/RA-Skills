## Description: <br>
This skill analyzes HD succulent images or videos from cameras, smartphones, local files, or URLs to detect black rot, melting, and stretching, then returns anomaly type, severity, confidence, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as home growers, greenhouse staff, and flower shop operators use this skill to screen succulent images or videos for black rot, melting, and stretching. Agents can also use it to query cloud-hosted historical analysis reports linked to the current workspace account identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads local media or submitted URLs to a third-party cloud analysis service. <br>
Mitigation: Use only images, videos, and URLs that are appropriate to share with the service, and confirm the service's data handling terms before installation. <br>
Risk: The skill can silently create or reuse an internal account identity and query account-linked report history. <br>
Mitigation: Install and run it only in the intended workspace/account context, and avoid shared workspaces when report history should remain separate. <br>
Risk: Service tokens and account identifiers may be stored in the workspace data directory. <br>
Mitigation: Restrict access to the workspace data directory and remove or rotate stored credentials after use when the workspace is shared or disposable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-succulent-special-state-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis results and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports basic, standard, and json detail modes; can save output to a file when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
