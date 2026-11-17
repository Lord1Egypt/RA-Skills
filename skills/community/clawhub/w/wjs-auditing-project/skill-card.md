## Description:

Use when the user asks to audit what's wrong with a project, "make it right", "看看项目出了什么问题", "为什么用户的需求还没上线", "为什么没提交App Store", "为什么没新build", or wants a holistic state-of-the-project check covering unmerged branches, stalled PRs, failed GitHub Actions, stale builds, plan drift (TODOS.md / ROADMAP), unreleased commits, and log errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to audit repository state, open work, CI, release readiness, plan drift, and relevant diagnostics before deciding what to fix. It presents a grouped checklist first and proceeds to fixes only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects broad repository, GitHub, and local macOS/Xcode diagnostic data during audits.

Mitigation: Use it only where that audit scope is acceptable, and review the generated checklist before approving any follow-up work.

Risk: The investigation can contact the configured git remote through a fetch operation while otherwise being framed as read-only.

Mitigation: Run it only when network contact with the configured remote is acceptable for the project.

Risk: Confirmed fix steps may involve merges, tags, stash changes, version bumps, or release preparation.

Mitigation: Require explicit confirmation before those actions and review the resulting diffs, release notes, and commands before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-auditing-project)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown checklist with supporting shell commands, code changes, configuration edits, and concise guidance when fixes are confirmed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Investigation output is read-only checklist guidance; fix output depends on explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
