## Description: <br>
Manage and standardize trading decision records, extract lessons, and support history retrieval and comparison within the PAI trading system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WuZiMaKi](https://clawhub.ai/user/WuZiMaKi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Trading agents and developers use this skill to structure persistent trading memory, including decision logs, state snapshots, trading rules, and mistakes. It supports routine review, lesson extraction, history comparison, and scheduled cleanup of trading memory records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent workspace memory maintenance can archive, delete, or alter project memory records if automatic cleanup is enabled too broadly. <br>
Mitigation: Set MG_WORKSPACE to a narrow project directory, run dry-runs before apply-mode or cron runs, and keep backups or snapshots. <br>
Risk: Retained trading memory may include stale, duplicate, or low-quality records that affect future decision review. <br>
Mitigation: Apply the documented daily and weekly review protocol and confirm a retention and deletion policy for archived or retired memories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WuZiMaKi/trading-memory-management) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with file path conventions and maintenance protocols] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines daily and weekly memory maintenance routines for trading records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
