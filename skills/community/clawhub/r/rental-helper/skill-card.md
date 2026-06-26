## Description: <br>
Rental Helper helps users manage rental searches by recording listings, calculating budgets, comparing options, reviewing rental pitfalls, recommending listings, importing data, parsing web pages or images, and optionally crawling rental sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sosshuai](https://clawhub.ai/user/sosshuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to organize a housing search, compare rental options, calculate move-in and monthly costs, record viewing notes, and surface practical rental-checklist guidance. It can also help parse listing URLs, screenshots, CSV or spreadsheet imports, and rental-site crawl results when those workflows are appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some data-fetching workflows can present sample or unverified listing data as if it were live rental inventory. <br>
Mitigation: Treat fetched listings as leads only, verify each listing against the original rental platform, and prefer manual listing entry for decisions that affect payments or lease commitments. <br>
Risk: Logged-in scraping can create site, account, or terms-of-service risk. <br>
Mitigation: Use interactive or logged-in crawling only after reviewing the target site's rules and accepting the account risk; avoid sharing credentials with the agent. <br>
Risk: The skill can store sensitive rental-search details such as phone numbers, exact addresses, screenshots, commute notes, and viewing notes in local rental-data files. <br>
Mitigation: Store only necessary details, review local files before sharing the workspace, and remove sensitive contact, address, or image data when it is no longer needed. <br>


## Reference(s): <br>
- [Rental Pitfall Guide](references/pitfall-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sosshuai/rental-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown, including tables, summaries, command suggestions, and local JSON-backed rental records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local rental listing and viewing data files under the user's rental-data workspace.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
