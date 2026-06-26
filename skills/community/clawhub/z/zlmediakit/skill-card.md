## Description: <br>
Tracks ZLMediaKit repository updates, recent issues and pull requests, and supports source-code analysis for users reviewing ZLMediaKit activity or implementation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feixintianxia](https://clawhub.ai/user/feixintianxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep a local ZLMediaKit checkout current, summarize recent GitHub issues and pull requests, and ask for source-level analysis of streaming modules such as RTSP/RTMP, WebRTC, and network I/O. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts GitHub, clones or updates the ZLMediaKit repository, and writes a local report. <br>
Mitigation: Run it with a dedicated WORKSPACE_DIR and review sync or periodic workflows before execution. <br>
Risk: Using GITHUB_TOKEN for API access can expose a credential if it is mishandled. <br>
Mitigation: Use a low-scope token, keep it secret, and avoid placing it in prompts, reports, or shared logs. <br>
Risk: GitHub API limits or request failures can make issue and pull-request summaries incomplete. <br>
Mitigation: Check generated report warnings, configure GITHUB_TOKEN when needed, and rerun before relying on time-sensitive summaries. <br>


## Reference(s): <br>
- [ZLMediaKit GitHub repository](https://github.com/ZLMediaKit/ZLMediaKit) <br>
- [ClawHub skill page](https://clawhub.ai/feixintianxia/zlmediakit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown reports with command snippets and source-code path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write zlmediakit_report.md in WORKSPACE_DIR and may clone or update a local ZLMediaKit checkout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
