## Description: <br>
Batch queries courier logistics information for multiple tracking numbers through the Xdccy API and can return console summaries or export result files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdccycom](https://clawhub.ai/user/xdccycom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, support teams, and operations teams use this skill to query logistics status for one or many courier tracking numbers, including SF shipments that require a phone-tail value. It can summarize results for review or export logistics data for customer and internal follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment identifiers, optional phone-tail digits, and API credentials are sensitive. <br>
Mitigation: Use limited credentials where possible, provide only shipment data needed for the task, and avoid storing credentials in shared prompts, files, or shell history. <br>
Risk: Exported result files may contain detailed logistics history and courier contact information. <br>
Mitigation: Protect generated XLSX, CSV, TXT, or JSON files, restrict access to intended recipients, and delete files when they are no longer needed. <br>
Risk: The skill sends tracking data to a third-party API operated by xdccy.com. <br>
Mitigation: Install and run the skill only when the user trusts xdccy.com and the configured API account or channel. <br>


## Reference(s): <br>
- [Input format specification](references/input-format.md) <br>
- [小递查查 API and credential portal](https://xdccy.com) <br>
- [ClawHub release page](https://clawhub.ai/xdccycom/skill-batchqueryexpress) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Console text, JSON, and optional XLSX, CSV, TXT, or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PlatformID, MemberID, and APIKey credentials; exported files may include shipment history and courier contact details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
