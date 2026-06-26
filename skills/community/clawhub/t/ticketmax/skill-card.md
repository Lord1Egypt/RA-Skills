## Description: <br>
Print markdown files to an ESC/POS thermal receipt printer over TCP, USB, or serial. Supports headings, bold, underline, tables, images, QR codes, paper cuts, and buzzer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yatesdr](https://clawhub.ai/user/yatesdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use Ticketmax to turn markdown reports, receipts, alerts, and summaries into physical ESC/POS thermal-printer output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can send sensitive or unintended content to a real configured printer. <br>
Mitigation: Confirm PRINTER_ADDR before use and review sensitive text before printing. <br>
Risk: Installing the latest ticketmax package can reduce supply-chain reproducibility. <br>
Mitigation: Use a pinned or reviewed ticketmax version when reproducible deployment matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yatesdr/ticketmax) <br>
- [Ticketmax Homepage](https://github.com/yatesdr/ticketmax) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and printer-oriented content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured PRINTER_ADDR and the ticketmax command; output may trigger physical printing, paper cuts, QR codes, images, and buzzer actions.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
