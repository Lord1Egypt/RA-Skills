## Description: <br>
Use this skill when the user needs public business emails, phone numbers, social profiles, source URLs, and crawl diagnostics from website domains or URLs through the Website Email Scraper & Phone Finder Apify actor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and business operations teams use this skill to run public website contact extraction through Apify and return email, phone, social profile, source URL, and crawl diagnostic rows for lead enrichment or CRM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted domains and URLs are sent to Apify for contact extraction, and returned emails, phone numbers, and social profiles may be privacy-sensitive. <br>
Mitigation: Use the skill only for appropriate public website contact extraction, limit collection to necessary fields, and apply retention, consent, and outreach compliance controls. <br>
Risk: The actor can include person-like emails and personal LinkedIn profile URLs when personal data extraction is enabled. <br>
Mitigation: Set includePersonalData=false when business inboxes are sufficient or personal contact data is not needed. <br>
Risk: Apify actor runs can incur usage costs. <br>
Mitigation: Set a run budget with maxTotalChargeUsd through the script's --budget-usd option and review RUN_SUMMARY when fewer rows are returned than requested. <br>
Risk: The skill requires an Apify API token. <br>
Mitigation: Provide APIFY_TOKEN through the environment or a secret manager and do not hardcode or print full tokens in user-facing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/website-email-scraper-apify) <br>
- [Project homepage](https://github.com/hundevmode/apify-website-email-scraper-agent-skill) <br>
- [Apify actor store page](https://apify.com/x_guru/website-email-phone-finder) <br>
- [Apify actor console source](https://console.apify.com/actors/kWfD7C0WpHtIt8VAh/source) <br>
- [Input and Output Contract](references/input-output-contract.md) <br>
- [Sample Input](references/sample_input.json) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash examples and JSON actor results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN. The runner returns JSON containing ok, actorId, fetchedAt, inputUsed, itemCount, and rows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
