## Description: <br>
Tao hop dong helps an agent look up Vietnamese business tax information from masothue.com, write contract rows to Google Sheets, and create related Odoo CRM records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minhduongqngai](https://clawhub.ai/user/minhduongqngai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business operations teams use this skill to create contract tracking records from Vietnamese tax identifiers. The agent gathers company details from masothue.com, appends a structured row to a Google Sheet, and creates or updates matching Odoo CRM customer and opportunity records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can write contract rows to Google Sheets and create persistent Odoo CRM customer and opportunity records. <br>
Mitigation: Before use, verify the Google account, spreadsheet target, Odoo database, and connector code, and require explicit confirmation or a dry run before any sheet update or CRM record creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minhduongqngai/taohopdong) <br>
- [masothue.com](https://masothue.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated Google Sheets access through gog and an available Odoo connector before write operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
