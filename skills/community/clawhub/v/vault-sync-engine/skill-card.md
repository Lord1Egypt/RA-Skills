## Description: <br>
知识库同步引擎 helps agents guide Obsidian vault synchronization across devices with Git-based workflows, selective configuration syncing, conflict handling, and sync health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical Obsidian users, and knowledge-management teams use this skill to select a vault synchronization approach, configure Git or cloud sync boundaries, detect conflicts, and preserve plugin configuration across devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated Git workflows can modify, commit, and push private Obsidian notes. <br>
Mitigation: Run commands only on a confirmed vault path, inspect pending changes before committing, and verify the configured remote repository before any push. <br>
Risk: Recurring cron or Task Scheduler automation can publish unintended note changes without a fresh user check. <br>
Mitigation: Keep automatic sync disabled unless the user explicitly accepts recurring commits and pushes for that vault. <br>
Risk: Incorrect sync boundaries can expose device-specific plugin settings or omit needed notes and attachments. <br>
Mitigation: Review .gitignore and plugin configuration rules before syncing, especially for .obsidian paths and attachment folders. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Git, cron, Task Scheduler, .gitignore, and conflict-resolution workflows for a user-provided Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
