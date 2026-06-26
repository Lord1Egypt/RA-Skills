## Description: <br>
Audits a project's repository, pull requests, CI, release state, plans, and app logs, then presents a grouped checklist before making any confirmed fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to understand why project work is stalled, why changes have not shipped, or what needs attention before a release. It is especially tailored to repository, GitHub Actions, pull request, TestFlight/App Store, plan-drift, and local app-log audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill audits the current project and may inspect repository state, GitHub state, build metadata, release history, and local app logs. <br>
Mitigation: Confirm the agent is running in the intended repository and signed into the intended GitHub account before invocation. <br>
Risk: After the checklist is confirmed, proposed fixes may include pushes, merges, tags, releases, stash changes, or branch actions. <br>
Mitigation: Review the grouped checklist and approve only the specific actions that should proceed. <br>
Risk: Release and App Store/TestFlight steps can require human-controlled signing and submission actions. <br>
Mitigation: Use the skill's human-action prompts for release submission commands instead of delegating signing or App Store submission to the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-auditing-project) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown checklist and concise summaries with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a two-phase workflow: read-only audit checklist first, then confirmed fixes with verification.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
