## Description: <br>
Generates a daily 21:30 fixed-income-plus product review report covering 87 products, track rankings, and top and bottom attribution analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wesdaliang](https://clawhub.ai/user/wesdaliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investment analysts and operations teams use this skill to gather Wind data for 87 fixed-income-plus products and produce a Markdown review with per-track dashboards, rankings, and attribution notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact documents an every-60-second cron task that posts to chat, which is broader than the stated daily 21:30 reporting purpose. <br>
Mitigation: Before installation or use, confirm whether the cron job exists and disable it or rescope it to the intended daily schedule. <br>
Risk: The skill depends on Wind data access and may create API quota, cost, or authorization issues if used without the right account permissions. <br>
Mitigation: Use only with authorized Wind access, monitor API usage, and set batch limits appropriate for the account. <br>
Risk: Financial reports can be misleading if the product list or returned market data is incomplete or stale. <br>
Mitigation: Validate the 87-product list and review Wind query results before relying on the generated report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wesdaliang/xqant-daily-gushouplus-report) <br>
- [Product codes](references/product_codes.md) <br>
- [Wind function reference](references/wind_functions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with tables, attribution notes, and inline shell commands for cron execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Wind data queries and product code validation; report tables omit product code columns in the final display.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
