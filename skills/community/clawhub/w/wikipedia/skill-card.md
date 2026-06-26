## Description: <br>
Access Wikipedia via MCP to search articles, retrieve summaries, fetch random facts, and generate dinosaur-specific facts for research and general knowledge workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanfoglia](https://clawhub.ai/user/evanfoglia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can add a local MCP server that lets an assistant search Wikipedia, retrieve article summaries, return random articles, and produce dinosaur or prehistory facts with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server sends search queries and requested article titles to Wikipedia over outbound network requests. <br>
Mitigation: Review whether queries may contain sensitive information before use and allow network access only where Wikipedia lookups are acceptable. <br>
Risk: Installation requires the Python requests package. <br>
Mitigation: Install dependencies in a managed environment and review package sources according to local dependency policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evanfoglia/wikipedia) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/evanfoglia) <br>
- [Wikipedia REST API endpoint](https://en.wikipedia.org/api/rest_v1) <br>
- [MediaWiki Action API endpoint](https://en.wikipedia.org/w/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [MCP tool responses containing plain text, markdown headings, source links, and optional image markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are capped by the tool limit; responses include links back to Wikipedia source articles when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
