## Description: <br>
Self improving helps an agent learn from explicit corrections, self-reflection, and repeated patterns by maintaining local memory files for preferences, lessons, and scoped project or domain rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Keyserkazi1](https://clawhub.ai/user/Keyserkazi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent keep transparent, local execution-improvement memory across tasks. It is most useful when the agent receives corrections, finds a reusable lesson, or needs to retrieve confirmed preferences and scoped project patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can influence future agent behavior in ways the user may not expect. <br>
Mitigation: Enable the skill only when persistent memory is desired, keep learned rules visible in ~/self-improving/, and review or delete entries periodically. <br>
Risk: Corrections or preferences could accidentally include secrets, sensitive personal data, or third-party information. <br>
Mitigation: Do not store credentials, financial data, health data, biometric information, third-party details, location routines, or access patterns; remove any such entry immediately if it appears. <br>
Risk: Workspace steering files such as AGENTS.md, SOUL.md, or HEARTBEAT.md may be changed during setup. <br>
Mitigation: Inspect proposed steering-file edits before use and keep setup changes scoped to the self-improving memory behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Keyserkazi1/self-improving-100) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Learning mechanics](artifact/learning.md) <br>
- [Memory operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-management instructions and file templates; no credentials or extra binaries are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
