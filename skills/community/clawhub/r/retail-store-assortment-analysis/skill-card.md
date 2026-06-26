## Description: <br>
Analyzes retail assortment display performance by comparing SKU attention, trial depth, customer intent dispersion, and conversion efficiency from store BI data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators, analysts, and store performance teams use this skill to compare store assortment engagement and conversion metrics across periods. It helps identify assortment attractiveness, trial depth changes, customer intent concentration, and SKU conversion efficiency from BI data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an unbundled local API client from a hard-coded personal path before reading store BI data. <br>
Mitigation: Review or replace the external API client before installation and run only in an environment where the local client is trusted. <br>
Risk: The skill accesses store BI data through the referenced dashboard endpoint. <br>
Mitigation: Use only with authorization for the referenced store data and confirm data handling requirements before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-store-assortment-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Console text report with structured analysis sections and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces period-over-period retail BI analysis based on store ID and date range inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
