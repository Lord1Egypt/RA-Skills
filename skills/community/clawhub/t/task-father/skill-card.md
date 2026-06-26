## Description: <br>
Generator for file-based task state machines (registry + task folders + lifecycle state + queue files + cron specs/jobs) for long-running work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moodykong](https://clawhub.ai/user/moodykong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create durable task folders, registries, lifecycle state, queue files, and optional OpenClaw cron jobs for long-running work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent OpenClaw cron prompts that continue running after setup. <br>
Mitigation: Review cron jobs before enabling them, inspect OpenClaw cron jobs regularly, and remove them when work is complete. <br>
Risk: Cron-name handling can write or delete files outside the intended cron folder. <br>
Mitigation: Use only simple cron names with letters, numbers, underscores, and hyphens; avoid slashes, absolute paths, and '..'. <br>
Risk: Generated task files and queues may expose sensitive task details if users place secrets in them. <br>
Mitigation: Avoid placing secrets in generated task files or queues until stronger path validation and confirmation controls are added. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown task records, JSON/JSONL state files, configuration files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace task folders, registry entries, queue files, and optional OpenClaw cron specs/jobs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
