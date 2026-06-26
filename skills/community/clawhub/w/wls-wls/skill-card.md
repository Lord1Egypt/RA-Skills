## Description: <br>
WLS runtime engineer skill for worker lifecycle, reload versus restart decisions, process cleanup, and runtime stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and runtime engineers use this skill to diagnose WLS worker lifecycle, dispatcher, process cleanup, reload, restart, and orchestration issues while preserving long-running runtime stability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation can use the wrong WLS port or leave a dedicated test instance running after the session. <br>
Mitigation: Use a unique test instance on port 9502 or higher, confirm the port and instance name before validation, and verify the instance is stopped afterward. <br>
Risk: Reload, restart, or process cleanup advice can disrupt active workers if applied without lifecycle context. <br>
Mitigation: Trace the affected worker, dispatcher, orchestrator, or master path first, choose reload versus restart based on the changed runtime surface, and avoid blind process killing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/wls-wls) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aiweline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code and shell-command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation evidence and cleanup confirmation when WLS testing is performed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
