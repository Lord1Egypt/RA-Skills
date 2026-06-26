## Description: <br>
Socialdatax Douyin helps agents retrieve Douyin hot-search, content, comment, reply, creator, creator-post, and creator-series data through the SocialDataX service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform read-only Douyin research, including hot-search lookup, work discovery, details, comment and reply analysis, and creator profile or content lookups. It is suited for workflows that have a SocialDataX API key and need structured Douyin data without account-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands run the external npm package socialdatax-skills and use the SOCIALDATAX_API_KEY. <br>
Mitigation: Verify trust in SocialDataX and the npm package before installing or executing commands, and provide the API key only in the intended environment. <br>
Risk: Douyin research results may be incomplete, paginated, or dependent on SocialDataX service availability and API access. <br>
Mitigation: Use the documented pagination options where available and treat returned data as service-provided research evidence rather than a complete platform record. <br>
Risk: Misuse could imply account interaction even though the skill is intended for read-only research. <br>
Mitigation: Keep use within the documented safety boundary: no login, posting, liking, commenting, local browser-data access, API-key storage, or account changes. <br>


## Reference(s): <br>
- [SocialDataX homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-douyin) <br>
- [Publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY plus node and npm; the skill describes read-only data retrieval commands.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
