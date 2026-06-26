## Description: <br>
Query-Skills helps agents search and discover OpenClaw skills with bilingual keyword search, multi-source lookup, filters, recommendations, and skill detail views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find OpenClaw skills by keyword, tag, author, popularity, relevance, or related-skill recommendations, then inspect details before installation or use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to ClawHub and, on fallback, to skills.volces.com. <br>
Mitigation: Avoid entering secrets, private project names, customer identifiers, or other sensitive terms as queries. <br>
Risk: The security guidance flags raw query logging and dependency hygiene concerns. <br>
Mitigation: Prefer an updated release that removes raw query logging and upgrades or pins axios before sensitive or managed use. <br>


## Reference(s): <br>
- [Query-Skills ClawHub release page](https://clawhub.ai/hgta23/query-skills) <br>
- [Publisher profile](https://clawhub.ai/user/hgta23) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style command-line text with search results, skill details, recommendations, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call ClawHub and fallback skill-search services using the user's query.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
