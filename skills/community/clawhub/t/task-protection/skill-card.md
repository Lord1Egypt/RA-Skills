## Description:

Task Protection provides task lifecycle management for recurring, critical, external, user-delegated, or long-running operations with tracking, failure analysis, progress logging, and completion feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredming-2026](https://clawhub.ai/user/alfredming-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register, monitor, and report on important work such as recurring system tasks, critical configuration changes, external messages, API calls, user-delegated work, and long-running operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can perform under-disclosed external messaging and network calls.

Mitigation: Review scripts before installing and make external sends opt-in with explicit operator approval.

Risk: The daily news script includes a fixed Tavily key and embedded Feishu recipient.

Mitigation: Remove fixed credentials and recipients, rotate any exposed credentials, and require runtime configuration for outbound services.

Risk: Task state and logs may retain operational details or sensitive user-provided task content.

Mitigation: Decide what task data may be logged, set retention rules, and avoid recording secrets or private content.

Risk: Unsafe file handling around task identifiers can affect local task state and log paths.

Mitigation: Validate task IDs against a restricted character set before creating or updating files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alfredming-2026/skills/task-protection)
- [Quickstart](docs/QUICKSTART.md)
- [Task Trigger Criteria](docs/task-trigger-criteria.md)
- [AI Task Registration Guide](docs/ai-task-registration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks, JSON task status files, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local task state and log files when its shell helpers are used.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
