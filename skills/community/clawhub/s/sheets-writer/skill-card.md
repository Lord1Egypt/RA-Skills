## Description: <br>
Google Sheets Data Writer. Use when the user wants to append rows, update cells, or automate spreadsheet data pipelines against a pre-configured target sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to configure a target Google Sheet, append rows, update specific cells, and verify spreadsheet data changes through the porteden CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet write operations can overwrite existing cell values or add incorrect data. <br>
Mitigation: Prefer append for new rows, review any multi-cell write with the user before execution, and read the target range back after writing. <br>
Risk: Drive-enabled credentials may allow access beyond the intended spreadsheet. <br>
Mitigation: Use a dedicated Google account or porteden profile limited to the required sheets, and confirm the user trusts the porteden CLI before installation or authentication. <br>
Risk: Untrusted input values can be interpreted as spreadsheet formulas. <br>
Mitigation: Use --raw for values from users, agents, or external sources so formula-like strings are written as literals. <br>


## Reference(s): <br>
- [Google Sheets File Automation on ClawHub](https://clawhub.ai/porteden/sheets-writer) <br>
- [PortEden](https://porteden.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes compact JSON output, credential scoping, append-first writes, and read-back verification.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
