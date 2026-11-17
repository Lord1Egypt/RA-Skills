## Description:

Yintai Task Runner polls Yintai/OpenClaw task APIs, claims available tasks, updates task status, and produces ZIP deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bossandy123](https://clawhub.ai/user/bossandy123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate Yintai/OpenClaw task polling, task claiming, status updates, and deliverable upload. It is intended for explicit task-runner workflows where the operator controls credentials, API endpoint, polling cadence, and task filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically claim paid tasks and mark them completed while producing placeholder deliverables.

Mitigation: Run only after manual review, use once-only execution during validation, and do not allow paid or production task claims unless placeholder completion is acceptable.

Risk: Credentials and task data are sent to the configured task API endpoint.

Mitigation: Use low-privilege Yintai credentials, provide secrets through environment variables, and keep TASK_API_BASE_URL pinned to a trusted HTTPS endpoint.

Risk: Cron or continuous polling can repeatedly claim tasks without further operator review.

Mitigation: Avoid cron and continuous mode until execution behavior is validated, and use minimum bounty and category filters with log monitoring when enabling automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bossandy123/skills/yintai-tasks-runner)
- [Artifact README](artifact/README.md)
- [API reference](artifact/references/api.md)
- [CLI usage](artifact/references/cli.md)
- [Configuration reference](artifact/references/config.md)
- [Usage guide](artifact/references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown status summaries, CLI/Python usage guidance, and ZIP deliverable files containing JSON metadata and text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus YINTAI_APP_KEY and YINTAI_APP_SECRET; optional configuration includes TASK_API_BASE_URL, TASK_POLL_INTERVAL, TASK_OUTPUT_DIR, minimum bounty, and category filters.]

## Skill Version(s):

1.1.6 (source: server release evidence; artifact frontmatter lists 1.1.0 and pyproject.toml lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
