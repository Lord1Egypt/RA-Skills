## Description: <br>
Professional SWOT analysis and competitive comparison powered by SWOTPal.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aprilelevengo](https://clawhub.ai/user/aprilelevengo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external business users, analysts, strategists, and developers use this skill to generate SWOT analyses, compare competitors, and retrieve saved SWOTPal analyses when an API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud/API mode can send and store SWOT topics, prompts, outputs, and saved analyses remotely without clear data-handling disclosure. <br>
Mitigation: Use local prompt mode for confidential strategy or internal company data unless the publisher documents retention, deletion, access controls, and an opt-out or local-only path. <br>
Risk: The configured SWOTPal API key could be exposed through local environment leakage or logs. <br>
Mitigation: Store the API key in a secret manager or protected environment variable, avoid sharing logs that include it, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [SWOTPal homepage](https://swotpal.com) <br>
- [SWOTPal API key setup](https://swotpal.com/openclaw) <br>
- [SWOTPal examples](https://swotpal.com/examples) <br>
- [ClawHub skill page](https://clawhub.ai/aprilelevengo/swotpal-swot-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aprilelevengo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown with section headings, numbered lists, links, and optional API result metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language; API mode may include editor URLs and remaining usage.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
