## Description: <br>
Use when installing, migrating, updating, validating, troubleshooting, or scheduling an automated arXiv paper digest inside an Obsidian Vault on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debtvc2022](https://clawhub.ai/user/debtvc2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this skill to install, update, validate, troubleshoot, and optionally schedule a Windows-based arXiv digest inside a confirmed Obsidian Vault. It helps preserve existing notes and generated outputs while guiding configuration and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update files inside an Obsidian Vault. <br>
Mitigation: Install only into the intended Vault, run the dry-run preview first, and require explicit approval before using force updates on an existing project. <br>
Risk: Optional summaries can send paper metadata and abstracts to DeepSeek when summary generation is enabled. <br>
Mitigation: Review config.yaml before scheduling and set summary_enabled to false or leave DEEPSEEK_API_KEY unset when external summarization is not desired. <br>
Risk: Optional Windows scheduling can create or replace a recurring background task. <br>
Mitigation: Use WhatIf for task registration previews and inspect any existing task name, action path, target Vault, and next run time before approving Force. <br>


## Reference(s): <br>
- [Operations Reference](references/operations.md) <br>
- [DeepSeek API Base URL](https://api.deepseek.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/debtvc2022/setup-obsidian-arxiv-daily) <br>
- [Publisher Profile](https://clawhub.ai/user/debtvc2022) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with PowerShell commands, configuration instructions, and validation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install or update files in a user-selected Obsidian Vault and may guide optional Windows Task Scheduler registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
