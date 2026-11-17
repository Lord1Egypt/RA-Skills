## Description:

Install and enforce a lightweight product-management workflow inside a code repo: feature-as-kanban boards, ROADMAP status tracking, branch/PR conventions, and an optional daily OpenClaw cron PM review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michailbul](https://clawhub.ai/user/michailbul)

### License/Terms of Use:


## Use Case:

Developers and agent teams use this skill to add a lightweight PM workflow to new or existing repositories, including roadmap status, per-feature kanban boards, bug intake, branch and PR conventions, and optional daily review automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron helper creates persistent agent automation.

Mitigation: Review the cron helper before use and choose the agent, timezone, schedule, and credentials intentionally.

Risk: The daily review message includes a hardcoded unpinned npx type-check command for apps/telegram.

Mitigation: Remove or replace the hardcoded check with a repository-appropriate, pinned validation command before enabling the cron helper.

Risk: The initialization workflow changes repository PM documentation and AGENTS.md conventions.

Mitigation: Run it only in repositories where the team wants this PM workflow, and review the generated docs and AGENTS.md changes before relying on them.

## Reference(s):

- [Repo Kanban PM on ClawHub](https://clawhub.ai/michailbul/skills/repo-kanban-pm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and repository documentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update repo PM files and optionally configure a recurring OpenClaw cron review.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
