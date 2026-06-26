## Description: <br>
Track vehicle expenses (gas, maintenance, parts) in Google Sheets and save related photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huchengtw](https://clawhub.ai/user/huchengtw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Vehicle owners and operators use this skill to record fuel, maintenance, repair, accessory, and purchase expenses, including mileage, costs, quantities, notes, and receipt photos. It supports Google Sheets for shared tracking and local Excel files for offline tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Sheets access may write to an unintended spreadsheet or broader account scope if credentials are over-permissioned. <br>
Mitigation: Use a dedicated Google service account with access limited to the intended spreadsheet. <br>
Risk: Vehicle or category names can affect local save paths for Excel and photo files. <br>
Mitigation: Avoid vehicle and category names containing slashes, absolute paths, or '..' before running the skill. <br>
Risk: Dry-run mode may still change configuration when default-saving options or new categories are used. <br>
Mitigation: Do not treat dry-run as no-write until the config-save behavior is fixed; review configuration before and after previews. <br>


## Reference(s): <br>
- [Vehicle Expense Tracker on ClawHub](https://clawhub.ai/huchengtw/vehicle-tracker) <br>
- [Publisher profile: huchengtw](https://clawhub.ai/user/huchengtw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands; JSON preview output during dry run; spreadsheet rows, Excel files, and copied photo files during execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English, Traditional Chinese, and Japanese locales; supports metric and imperial unit systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
