## Description: <br>
Discover website URLs, feed entries, and latest publications by checking sitemap.xml, sitemaps.xml, atom.xml, and rss.xml before crawling a specific site. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosdelfino](https://clawhub.ai/user/carlosdelfino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover crawlable URLs, feed entries, and recent publications from a specific website before falling back to broader crawling or search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script runs on the host and makes outbound HTTP requests. <br>
Mitigation: Scope exec approvals to the bundled Node.js script and use one-time approval unless repeated use is intentional. <br>
Risk: Using the skill against localhost, private IP ranges, or sensitive internal domains can expose internal network information to the agent workflow. <br>
Mitigation: Use it on internal targets only when that access is intentional and authorized. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/carlosdelfino/rss-sitemap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the bundled Node.js preprocessor] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The preprocessor emits JSON resources and entries with source provenance for discovered sitemap, RSS, and Atom content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
