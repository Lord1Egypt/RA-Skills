## Description: <br>
The News Tool Free helps agents retrieve public news snapshots across 20 countries, including current headlines and up to 7 days of historical news, using a public news API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch public top-news snapshots by country, query recent historical snapshots, and prepare lightweight headline or overview summaries for personal news monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes some database and storage tasks into a news lookup workflow without explaining or implementing that scope. <br>
Mitigation: Use the skill only for public news lookup and do not rely on it for database operations, SQL queries, storage management, or architecture decisions. <br>
Risk: The skill makes external public API calls and supports callback_url-style inputs. <br>
Mitigation: Do not send secrets, private documents, internal URLs, confidential business data, or untrusted callback URLs through this skill. <br>
Risk: The security verdict is suspicious and the publisher guidance asks for clarification of external API and callback behavior. <br>
Mitigation: Review the skill before installation and require the publisher to clarify API, callback, database, and storage behavior before broader deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/the-news-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [The Hear country news API](https://www.thehear.org/api/country-view/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access, curl for HTTP requests, and optionally jq for JSON filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
