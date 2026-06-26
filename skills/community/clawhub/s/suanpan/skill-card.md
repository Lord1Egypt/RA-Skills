## Description: <br>
将用户自然语言交易描述转换为 suanpan CLI 命令，用于记账、消费、支出、收入、转账、查账和统计等个人财务任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinguobing](https://clawhub.ai/user/yinguobing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal finance users and agents use this skill to translate Chinese natural-language bookkeeping requests into suanpan CLI commands for recording, querying, updating, importing, and analyzing financial records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose commands that add, update, remove, import, or otherwise change persistent financial records. <br>
Mitigation: Require explicit user confirmation before executing mutating suanpan commands and keep backups of the finance database. <br>
Risk: The quick installer uses a curl-to-bash pattern. <br>
Mitigation: Inspect or pin the downloaded install script before running it, or build from source after review. <br>
Risk: Financial account names, transaction records, and related personal finance details may be sensitive. <br>
Mitigation: Avoid exposing private finance data in prompts, logs, shared transcripts, or generated command examples. <br>


## Reference(s): <br>
- [交易管理命令参考](references/commands.md) <br>
- [统计分析命令参考](references/analytics.md) <br>
- [数据管理命令参考](references/management.md) <br>
- [ClawHub skill page](https://clawhub.ai/yinguobing/suanpan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed suanpan CLI commands and brief guidance; users should review commands before execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
