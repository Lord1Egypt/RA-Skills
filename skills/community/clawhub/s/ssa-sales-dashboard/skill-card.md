## Description: <br>
Aggregates sales data from OKKI CRM and Campaign Tracker to generate weekly and monthly reports with alerts and Discord delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams use this skill to collect CRM and campaign metrics, calculate funnel performance and anomalies, and prepare scheduled weekly or monthly sales reports for internal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive CRM, sales, and campaign data. <br>
Mitigation: Review generated reports before distribution and avoid sending confidential customer or sales information to unapproved recipients. <br>
Risk: Reports and alerts can be prepared for Discord delivery on a schedule. <br>
Mitigation: Restrict Discord delivery to approved private channels and disable or review scheduled jobs when unattended reporting is not intended. <br>
Risk: The data collector depends on OKKI credentials and environment files. <br>
Mitigation: Confirm the intended OKKI workspace, credentials, token cache, and .env path before installation or execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cjboy007/ssa-sales-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON metric and push-instruction files, and Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include sensitive customer, sales, and campaign metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
