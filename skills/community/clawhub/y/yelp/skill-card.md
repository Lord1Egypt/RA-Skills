## Description: <br>
Search Yelp businesses and reviews, compare local options, and audit listing quality with official APIs, public pages, and safe action boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and local-business operators use this skill to find and compare Yelp businesses, analyze review signals, and prepare listing-quality audits with source-aware boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yelp API or public-page workflows can send business names, search terms, location hints, phone numbers, and optional filters to Yelp. <br>
Mitigation: Use live Yelp calls only when the user accepts sharing that local-search context, and confirm before sending phone numbers, exact addresses, or account-scoped listing data. <br>
Risk: API keys or signed request details could leak if copied into local notes or logs. <br>
Mitigation: Keep API keys out of markdown files and store only redacted endpoint paths, safe parameters, status, and timestamps in ~/yelp/. <br>
Risk: Yelp fields such as hours, price, transactions, and delivery or takeout flags may be stale or incomplete. <br>
Mitigation: Mark uncertainty and re-check operational claims close to booking, visiting, calling, or ordering. <br>
Risk: Owner-side listing work can imply account access or authority the agent does not have. <br>
Mitigation: Stay read-only by default; draft responses or audit recommendations only after the user confirms they are authorized. <br>


## Reference(s): <br>
- [ClawHub Yelp listing](https://clawhub.ai/ivangdavila/yelp) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill homepage](https://clawic.com/skills/yelp) <br>
- [Yelp API workflows](artifact/api-workflows.md) <br>
- [Yelp search playbook](artifact/search-playbook.md) <br>
- [Yelp review analysis](artifact/review-analysis.md) <br>
- [Yelp listing audit](artifact/listing-audit.md) <br>
- [Yelp access boundaries](artifact/access-boundaries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and comparison or audit tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should disclose whether evidence came from Yelp API, public pages, or both, and should mark stale, weak, or uncertain evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
