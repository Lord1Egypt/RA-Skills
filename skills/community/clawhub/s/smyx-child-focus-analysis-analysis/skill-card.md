## Description: <br>
Analyzes child study-area video from a smart desk lamp or tabletop camera to estimate per-minute focus scores, identify distraction periods, and summarize focus reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, parents, teachers, and agent operators use this skill to submit child study-area videos or video URLs for focus scoring, distraction-event reporting, and history lookup. It is intended as a visual behavior analysis aid, not a replacement for human educational judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child study videos, video URLs, and user identifiers are sent to the publisher's remote service. <br>
Mitigation: Use the skill only with guardian consent, share the minimum necessary media and identifiers, and confirm the publisher's retention and deletion practices before deployment. <br>
Risk: Cloud report history can be queried and may expose prior analysis records. <br>
Mitigation: Limit use to authorized accounts, verify who can access report history, and avoid running history queries in shared or untrusted environments. <br>
Risk: Login tokens may be stored locally as part of account handling. <br>
Mitigation: Review local token storage and account handling before installation, use dedicated credentials where possible, and rotate or revoke credentials if a workstation is shared or compromised. <br>


## Reference(s): <br>
- [Child focus analysis API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-focus-analysis-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text, with shell command examples for invoking the analysis and history-query scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include focus scores, per-minute score series, distraction events, report links, and persisted result files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
