## Description: <br>
Manage Todoist tasks via the `todoist` CLI (list, add, modify, complete, delete), with support for filters, projects, labels, and priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2mawi2](https://clawhub.ai/user/2mawi2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to help users manage Todoist tasks from the terminal, including listing, creating, modifying, completing, and deleting tasks. It is useful for productivity workflows that need Todoist CLI commands, filter syntax, project selection, labels, priorities, and local sync guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to complete, delete, or bulk-modify Todoist tasks. <br>
Mitigation: Review destructive or bulk task-modification commands before allowing the agent to run them. <br>
Risk: The Todoist CLI configuration stores an API token in ~/.config/todoist/config.json. <br>
Mitigation: Protect the local config file and avoid exposing the token in prompts, logs, screenshots, or shared terminal output. <br>
Risk: The skill depends on the Homebrew todoist-cli package and local todoist binary. <br>
Mitigation: Install only a trusted todoist-cli package and confirm the expected todoist binary is present before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2mawi2/todoist-task-manager) <br>
- [Todoist CLI project](https://github.com/sachaos/todoist) <br>
- [Todoist developer integrations settings](https://app.todoist.com/app/settings/integrations/developer) <br>
- [Todoist filter syntax](https://todoist.com/help/articles/introduction-to-filters-V98wIH) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Todoist task IDs, filters, project names, label names, priorities, due dates, and sync commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
