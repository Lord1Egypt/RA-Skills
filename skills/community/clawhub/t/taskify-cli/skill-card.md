## Description: <br>
Manage tasks and boards on Nostr relays via CLI to list, create, update, assign, complete, search, and export tasks with JSON support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ink-North](https://clawhub.ai/user/Ink-North) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Taskify task and board workflows from the command line, including reading, creating, updating, assigning, completing, importing, exporting, and searching tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on installing and executing the external taskify-nostr npm package. <br>
Mitigation: Install only after verifying the npm package and linked source repository, and prefer a user-local install on shared systems. <br>
Risk: Task data syncs through configured Nostr relays and relay changes affect where task traffic is sent. <br>
Mitigation: Use only relays you control or trust, and review relay add or remove commands before execution. <br>
Risk: AI-assisted Taskify commands can forward task text to an external AI backend. <br>
Mitigation: Use AI commands only with a trusted or self-hosted backend, and avoid sensitive boards unless that backend is approved. <br>
Risk: Some commands can delete, import, clear, or otherwise overwrite task and board state. <br>
Mitigation: Review destructive actions such as deletes, clear-completed, imports, cache clears, and relay changes before running them. <br>


## Reference(s): <br>
- [Taskify CLI page](https://clawhub.ai/Ink-North/taskify-cli) <br>
- [taskify-nostr npm package](https://www.npmjs.com/package/taskify-nostr) <br>
- [Taskify source repository](https://github.com/Solife-me/Taskify_Release) <br>
- [Full command flags](references/commands.md) <br>
- [Board and column operations](references/boards.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown, code] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON-oriented parsing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Taskify commands may return human-readable text or machine-readable JSON when supported by the --json flag.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
