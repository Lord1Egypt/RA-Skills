## Description: <br>
Scrape employee data from a logged-in SAP SuccessFactors browser session using browser automation when a user provides an employee ID and needs employee details from the SuccessFactors UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VenkataLokesh-dot](https://clawhub.ai/user/VenkataLokesh-dot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and business operators use this skill to retrieve visible employee profile details from an authorized, logged-in SAP SuccessFactors browser session. It is intended for browser-based lookup workflows where the user already has access to the relevant SuccessFactors records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive employee records from a logged-in SuccessFactors session. <br>
Mitigation: Install and use it only for users authorized to retrieve the requested employee records through their existing SuccessFactors permissions. <br>
Risk: Broad or batch employee lookups can disclose more HR data than needed. <br>
Mitigation: Limit batch processing to approved business workflows and return only the employee fields needed for the stated purpose. <br>
Risk: Browser Relay access could act on the wrong browser context. <br>
Mitigation: Keep Browser Relay scoped to the intended SuccessFactors tab before scraping profile data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VenkataLokesh-dot/sf-scrapper) <br>
- [Publisher profile](https://clawhub.ai/user/VenkataLokesh-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text with extracted employee fields and error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Only fields actually visible in the SuccessFactors UI should be returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
