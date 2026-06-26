## Description: <br>
Team Memory is a local Markdown-based team memory system for recording team member observations, maintaining profiles and distilled summaries, preparing 1:1s, and generating weekly, monthly, performance, and promotion materials while preserving v1 data compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jichengkai](https://clawhub.ai/user/jichengkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers and team leads use this skill to maintain local, evidence-based personnel notes and prepare 1:1, team status, performance, and promotion materials from Markdown records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to store sensitive employee observations and management notes in local files. <br>
Mitigation: Use it only when authorized to keep personnel notes, restrict access to the data directory, avoid public repositories or unencrypted sync, and define retention and deletion rules. <br>
Risk: Personnel notes can become misleading or inappropriate if they include unsupported judgments or non-job-relevant information. <br>
Mitigation: Record factual, job-relevant observations and distinguish evidence, inference, and recommendations when using notes for performance or promotion decisions. <br>
Risk: Initialization and migration scripts create or copy local files, including backups and member records. <br>
Mitigation: Review paths before execution, run the migration dry-run first, use --apply only after confirming the plan, and keep backups protected. <br>


## Reference(s): <br>
- [Team Memory Usage Guide](artifact/references/usage.md) <br>
- [Team Memory Upgrade and Compatibility Notes](artifact/references/upgrade.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jichengkai/team-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local Markdown records and configuration under the user's Team Memory data directory.] <br>

## Skill Version(s): <br>
2.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
