## Description: <br>
Sprint OS is a 5-minute sprint operating system for AI agents that runs ASSESS -> PLAN -> SCOPE -> EXECUTE -> MEASURE -> ADAPT -> LOG -> NEXT cycles with optional Convex integration for sprint tracking, metrics, and content deduplication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Batsirai](https://clawhub.ai/user/Batsirai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use Sprint OS to keep AI agents working in short, logged execution cycles that produce concrete artifacts. It can also log sprint activity locally or to an optional Convex backend for tracking, metrics, and content deduplication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages sustained autonomous sprint execution and may continue file or network work beyond the user's intended scope. <br>
Mitigation: Set a clear task scope, sprint limit, and approval rules for file changes, publishing, account actions, and network calls before enabling sprint mode. <br>
Risk: Local or remote sprint logs can contain sensitive project details, private prompts, customer data, or confidential business information. <br>
Mitigation: Review log content before sharing, avoid logging secrets or confidential data, and treat generated sprint logs as sensitive records. <br>
Risk: Optional Convex logging sends sprint details to a configured remote endpoint. <br>
Mitigation: Enable Convex logging only with a trusted endpoint, add authentication and access controls to the backend, and keep the endpoint configuration under user control. <br>


## Reference(s): <br>
- [Sprint OS ClawHub Page](https://clawhub.ai/Batsirai/sprint-os) <br>
- [Convex Documentation](https://convex.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write sprint-log.md locally and optionally send sprint records to a configured Convex endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
