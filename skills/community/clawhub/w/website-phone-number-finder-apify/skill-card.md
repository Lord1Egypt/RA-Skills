## Description:

Use this skill when the user needs public business phone numbers, tel links, optional emails, social profiles, source URLs, and crawl diagnostics from website domains or URLs through the Website Phone Number Finder Apify actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Apify website phone-number extraction from supplied domains or URLs, control spend, and return structured contact rows for lead enrichment, CRM, spreadsheet, BI, or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted websites and scraped contact results are sent to Apify, and optional settings can collect personal-data fields.

Mitigation: Use only when that data handling is acceptable, keep collection to the minimum needed, and set includePersonalData=false unless there is a clear lawful reason to collect personal-data fields.

Risk: The Apify token can authorize actor runs and may be exposed if passed directly on the command line or logged.

Mitigation: Use a narrowly scoped token through APIFY_TOKEN or a secrets manager, avoid printing the token, and prefer environment-based credentials over --apify-token.

Risk: Actor runs can incur Apify charges.

Mitigation: Set a budget guard with --budget-usd or maxTotalChargeUsd and inspect RUN_SUMMARY when results stop early.

Risk: Installing a third-party skill carries supply-chain risk.

Mitigation: Review the ClawHub evidence, file hashes, license, and source links before installation, and install only from the expected publisher profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/website-phone-number-finder-apify)
- [Publisher profile](https://clawhub.ai/user/hundevmode)
- [Project homepage](https://github.com/hundevmode/apify-website-phone-number-finder-agent-skill)
- [Apify actor store page](https://apify.com/x_guru/website-phone-number-finder)
- [Apify actor console source](https://console.apify.com/actors/HE8ML7ZqmGI6OtyFU/source)
- [Input and output contract](references/input-output-contract.md)
- [Sample input](references/sample_input.json)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON results with optional Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; supports domain or URL inputs, budget guard, result mode, crawl depth, optional email/social extraction, and personal-data filtering.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
