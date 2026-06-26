## Description: <br>
Queries QiBook for Chinese company registration details and person-company relationships, then returns Chinese Markdown results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinadaas-department](https://clawhub.ai/user/chinadaas-department) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify companies and retrieve Chinese business registration, shareholder, executive, investment, legal representative, and person-affiliation information from QiBook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, person names, and optional province information are sent to the configured QiBook API endpoint. <br>
Mitigation: Install and invoke the skill only when this external lookup is intended, and avoid submitting data that should not be shared with the QiBook service. <br>
Risk: A misconfigured QIBOOK_BASE_URL could direct lookup requests and credentials to an untrusted endpoint. <br>
Mitigation: Set QIBOOK_BASE_URL only to the official trusted QiBook endpoint before use. <br>
Risk: QIBOOK_ACCESS_KEY is an API credential used for lookup requests. <br>
Mitigation: Store and handle QIBOOK_ACCESS_KEY like other secrets, and do not expose it in prompts, logs, or shared outputs. <br>
Risk: Casual company, owner, shareholder, executive, legal representative, or person-affiliation requests may trigger the skill. <br>
Mitigation: Review the user intent before invocation and keep the query scope limited to the requested company, person, or province. <br>


## Reference(s): <br>
- [Qibook Company Profile on ClawHub](https://clawhub.ai/chinadaas-department/qibook-company-profile) <br>
- [QiBook API Access Portal](https://skill.qibook.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Chinese Markdown with tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QIBOOK_ACCESS_KEY and QIBOOK_BASE_URL; uses company name, person name, and optional province inputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
