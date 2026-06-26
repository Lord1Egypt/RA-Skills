## Description: <br>
Close the loop on long-running remote work: pick the right completion signal per platform (CI, EAS, deploy, releases), run monitoring in the background, notify on finish, and never treat trigger as success. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erergb](https://clawhub.ai/user/erergb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Wander to monitor long-running CI, build, deploy, and release tasks through the platform that owns the terminal status, then verify success or collect failure details before proceeding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External Wander scripts are cloned and executed outside the skill package. <br>
Mitigation: Verify the cloned Wander repository and scripts before installing or running them. <br>
Risk: GitHub CLI authentication may expose CI status and failed logs from repositories the user can access. <br>
Mitigation: Confirm the active GitHub account and repository scope before starting background monitoring. <br>
Risk: Background monitors can keep reading CI state until the watched job reaches a terminal status. <br>
Mitigation: Stop monitors that are no longer needed and review their terminal output before acting on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erergb/wander) <br>
- [Wander repository](https://github.com/ERerGB/wander) <br>
- [Wander v1 scope: GitHub Actions today](https://github.com/ERerGB/wander/blob/main/README.md#v1-scope-github-actions-today) <br>
- [Wander edge cases](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start background monitors and inspect CI status or failed logs through the user's authenticated tooling.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
