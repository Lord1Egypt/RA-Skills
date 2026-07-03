## Description: <br>
A workflow bundle for turning agent mistakes into durable system changes through daily reflection, candidate promotion, skill evolution, recidivism enforcement, and visibility reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h-mascot](https://clawhub.ai/user/h-mascot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this workflow to convert recurring agent mistakes into reviewed improvements through reflection logs, promotion checks, skill evolution, and visibility reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs an externally hosted self-improvement loop that can affect workspace memory, generated guidance, and scheduled behavior. <br>
Mitigation: Review the installer, source path, generated cron entries, affected workspace paths, and uninstall or rollback steps before enabling the workflow. <br>
Risk: Cron-driven reflection and skill-evolution behavior may promote unsuitable changes if review thresholds are too permissive. <br>
Mitigation: Use a test workspace first and enable cron only after confirming that proposed changes require appropriate human approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h-mascot/superada-workflow-recursive-self-improvem-t-pack) <br>
- [SuperAda workflow page](https://superada.ai/workflows/recursive-self-improvement-pack/) <br>
- [GitHub source path](https://github.com/h-mascot/superada-ai/tree/main/public/install/recursive-self-improvement-pack) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw workspace with cron support; review the external installer, memory mutation behavior, promotion thresholds, and rollback path before enabling scheduled runs.] <br>

## Skill Version(s): <br>
1.0.30 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
