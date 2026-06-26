## Description: <br>
Search academic papers and authors via the Scholar API (scholar.x49.ai) for paper discovery, author lookup, metadata retrieval, journal rankings, and filtered scholarly search across academic disciplines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahahaaaa123](https://clawhub.ai/user/wahahaaaa123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search scholarly literature, retrieve paper and author metadata, check venue quality signals, and format academic search results from the Scholar API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic search queries are sent to scholar.x49.ai. <br>
Mitigation: Install only when that third-party API use is acceptable for the user's data and workflow. <br>
Risk: The release includes a reusable built-in API token and credential examples that may expose or misuse a generic local secret. <br>
Mitigation: Remove or ignore the fallback token before use, set a Scholar-specific API key, and ensure Authorization examples use SCHOLAR_KEY or SCHOLAR_API_KEY. <br>


## Reference(s): <br>
- [Scholar API](https://scholar.x49.ai/api/v1) <br>
- [Scholar API Keys](https://scholar.x49.ai/docs?section=api-keys) <br>
- [ClawHub skill page](https://clawhub.ai/wahahaaaa123/scholar-search-x49) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns formatted paper, author, venue, citation, and identifier details from Scholar API responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
