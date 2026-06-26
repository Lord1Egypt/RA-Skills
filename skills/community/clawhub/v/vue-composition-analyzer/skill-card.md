## Description: <br>
Analyze Vue 3 Composition API usage by auditing reactivity patterns, composable design, ref and reactive choices, computed properties, watcher usage, and component lifecycle hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Vue 3 codebases, support migration from Options API, and identify Composition API anti-patterns in reactivity, composables, watchers, and lifecycle cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews files in the current project and may bring private source code into the agent's working context. <br>
Mitigation: Run it only from the intended Vue project and review the command scope before sharing results. <br>
Risk: Static grep-based checks can miss issues or report false positives in complex Vue codebases. <br>
Mitigation: Confirm findings with code review, Vue tooling, and project tests before applying changes. <br>


## Reference(s): <br>
- [Vue Composition Analyzer on ClawHub](https://clawhub.ai/charlie-morrison/vue-composition-analyzer) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and findings tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes project inspection commands, severity-ranked findings, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
