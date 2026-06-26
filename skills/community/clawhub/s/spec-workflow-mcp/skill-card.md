## Description: <br>
Serve spec-driven dev tools via MCP for AI-assisted workflows. Use when adding tasks, planning iterations, tracking completion, reviewing quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage spec-driven development workflows from an agent-assisted command line, including task capture, sprint planning, progress tracking, review notes, reminders, prioritization, timelines, reports, weekly reviews, search, status checks, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow notes are stored as plaintext local files and may contain sensitive project details if users enter them. <br>
Mitigation: Do not enter passwords, API keys, customer data, or confidential plans; periodically review or delete ~/.local/share/spec-workflow-mcp when the history is no longer needed. <br>
Risk: The bundled shell script creates and updates files in the configured data directory. <br>
Mitigation: Review the script and DATA_DIR setting before execution, and run it only in an environment where local workflow logging is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/spec-workflow-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Plain text and Markdown guidance with shell command examples; the bundled script can write plaintext logs and export JSON, CSV, or TXT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores workflow notes as plaintext under ~/.local/share/spec-workflow-mcp by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
