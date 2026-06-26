## Description: <br>
DeepLink Agentic helps agents create, monitor, retrieve, and iterate on deep real estate research tasks, including market analysis, land assessment, company and project research, policy interpretation, and property-industry reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dichanai](https://clawhub.ai/user/dichanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External real estate researchers, analysts, and business users use this skill to delegate long-running real estate research tasks to the DeepLink Agentic service, track progress, handle human-in-the-loop questions, and retrieve finished reports or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected user files are sent to agentic.dichanai.com for task execution. <br>
Mitigation: Use the skill only when the user accepts that data transfer, and avoid sending sensitive files unless they are explicitly needed for the task. <br>
Risk: Token renewal can print NEW_TOKEN values in cleartext. <br>
Mitigation: Treat AGENTIC_TOKEN and NEW_TOKEN as secrets, do not expose them in user-visible messages, and avoid renewal in shared or logged terminals. <br>
Risk: The skill supports sharing, scheduling, and deleting tasks. <br>
Mitigation: Require explicit user confirmation before sharing, scheduling, deleting, or aborting a task, and verify the target chat_id before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dichanai/real-estate-deep-research) <br>
- [DeepLink Agentic service](https://agentic.dichanai.com) <br>
- [DeepLink Agentic API documentation](https://agentic.apifox.cn/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, status text, JSON API responses, file listings, and download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce long-running task identifiers, status summaries, human-in-the-loop prompts, and temporary file download links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
