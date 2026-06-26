## Description: <br>
Use this skill when the user needs public business phone numbers, tel links, optional emails, social profiles, source URLs, and crawl diagnostics from website domains or URLs through the Website Phone Number Finder Apify actor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to run public website contact extraction through Apify, control crawl and budget settings, and return structured phone lead rows for spreadsheets, CRM, BI, or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target domains or URLs are sent to Apify for public contact extraction. <br>
Mitigation: Install and run the skill only when third-party Apify crawling is intended for the target websites. <br>
Risk: Runs can incur Apify usage charges. <br>
Mitigation: Use --budget-usd or Apify maxTotalChargeUsd to cap spend before launching a run. <br>
Risk: Optional settings can collect personal LinkedIn/profile-like data or person-like emails. <br>
Mitigation: Set includePersonalData=false or pass --no-personal-data unless collection is lawful and policy-compliant; enable email extraction only when it is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/website-phone-number-finder-apify) <br>
- [Project homepage](https://github.com/hundevmode/apify-website-phone-number-finder-agent-skill) <br>
- [Website Phone Number Finder Apify actor](https://apify.com/x_guru/website-phone-number-finder) <br>
- [Apify actor console source](https://console.apify.com/actors/HE8ML7ZqmGI6OtyFU/source) <br>
- [Input and output contract](references/input-output-contract.md) <br>
- [Sample input](references/sample_input.json) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON runner output with agent-facing Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns run status, actor ID, timestamp, normalized input, item count, and rows containing phone numbers, source URLs, optional contact fields, social links, and crawl diagnostics.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
