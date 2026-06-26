## Description: <br>
Format tabular data as ASCII box tables for Telegram. Stdin-only input eliminates shell injection risks. Handles smart column sizing, text wrapping, and proper padding for monospace display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NaLG](https://clawhub.ai/user/NaLG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn pipe-delimited rows into Telegram-friendly monospace tables for chat updates, status summaries, and compact reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive table data could be included in generated output and then shared in Telegram. <br>
Mitigation: Only pipe or paste data intended for the table and review the generated output before sending it. <br>
Risk: The pipe character is used as the column delimiter and cannot appear safely inside cell content. <br>
Mitigation: Remove or replace pipe characters in cell values before formatting the table. <br>
Risk: Wide characters such as emoji or CJK text may not align consistently in Telegram monospace rendering. <br>
Mitigation: Preview the output in the target Telegram client and use mobile ASCII mode when compatibility matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NaLG/telegram-ascii-table) <br>
- [Publisher profile](https://clawhub.ai/user/NaLG) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell examples and generated plain-text ASCII or Unicode table output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads table rows from stdin; supports desktop Unicode mode, mobile ASCII mode, and custom width.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
