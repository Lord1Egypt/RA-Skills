## Description: <br>
Converts pasted PySpark `.show()` output into tab-separated text that can be copied directly into Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dilicloud11](https://clawhub.ai/user/dilicloud11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and analysts use this skill to convert PySpark `.show()` table output into a tab-delimited format for Excel. The skill is intended for formatting only and does not analyze or modify the data values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad table-formatting phrases and transform pasted table text that was not intended for conversion. <br>
Mitigation: Review the pasted input before use and apply the skill only to PySpark `.show()` output that should be converted to tab-separated text. <br>
Risk: Pasted table data is processed in the chat context, which may expose sensitive values to the agent session. <br>
Mitigation: Avoid pasting sensitive data, or sanitize the table before asking the agent to format it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dilicloud11/pyspark-to-excel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown fenced code block containing tab-separated text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formatting-only conversion; strips PySpark table border lines and trailing row-count notices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
