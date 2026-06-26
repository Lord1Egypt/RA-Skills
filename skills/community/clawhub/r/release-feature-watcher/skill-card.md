## Description: <br>
Use when the user wants to monitor a technical feature, bugfix, model/API update, changelog, release, package version, or PR and be notified only when a specific actionable condition is met. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abe238](https://clawhub.ai/user/abe238) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create quiet, actionable watchers for releases, changelogs, packages, models, APIs, GitHub issues, and pull requests. It helps define readiness conditions, record baselines, configure checks, and produce concise notifications only when the watched change is ready or the check is blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A vague watcher condition can produce noisy or non-actionable notifications. <br>
Mitigation: Define a specific source, readiness condition, baseline, schedule, and next action before creating the watcher. <br>
Risk: Long-running watchers can remain active after the user no longer needs them. <br>
Mitigation: Set an expiry or self-removal rule and periodically review watcher configs under ~/.hermes/watchers. <br>
Risk: Cron jobs created for monitoring can outlive their useful purpose. <br>
Mitigation: Remove cron jobs when the watched release, fix, or feature has shipped, or when the source is no longer relevant. <br>


## Reference(s): <br>
- [Release Feature Watcher on ClawHub](https://clawhub.ai/abe238/release-feature-watcher) <br>
- [Condition Patterns](references/condition-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown watcher cards and alerts, JSON watcher configuration, and shell or Python command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quiet-by-default behavior; watchers alert only when the readiness condition is met or checking is blocked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
