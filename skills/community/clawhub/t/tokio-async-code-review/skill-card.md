## Description: <br>
Reviews tokio async runtime usage for task management, sync primitives, channel patterns, and runtime configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust projects that use Tokio, async/await, spawned tasks, channels, async synchronization, runtime configuration, and related tower, hyper, or tokio-util integration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a companion review-verification-protocol skill before findings are reported. <br>
Mitigation: Install the companion skill from a trusted source and complete its pass conditions before relying on review results. <br>
Risk: Async code-review guidance can produce misleading findings if the dependency surface, runtime model, or blocking inventory gates are skipped. <br>
Mitigation: Complete the documented gates and require file:line evidence for every reported issue. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/tokio-async-code-review) <br>
- [Task Management](references/task-management.md) <br>
- [Sync Primitives](references/sync-primitives.md) <br>
- [Channels](references/channels.md) <br>
- [Pinning, Cancellation, and Async Internals](references/pinning-cancellation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings with file and line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings use Critical, Major, Minor, or Informational severity labels.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
