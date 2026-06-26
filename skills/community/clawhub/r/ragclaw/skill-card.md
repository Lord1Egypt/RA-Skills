## Description: <br>
Local-first knowledge base skill for indexing, searching, and managing documents, code, and web pages with offline embeddings and SQLite storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emdzej](https://clawhub.ai/user/emdzej) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build and query a local knowledge base from project files, documentation, and selected web pages without relying on external APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index local files and URLs, which may capture sensitive or unintended content if broad paths or crawl settings are used. <br>
Mitigation: Index narrow folders and known URLs, avoid secrets and broad home directories, use include/exclude filters and crawl limits, and remove or prune unintended sources. <br>
Risk: The skill depends on the external @emdzej/ragclaw-cli package for execution. <br>
Mitigation: Install and run the CLI only when the publisher and package are trusted. <br>
Risk: Web crawling can fetch more pages than intended if crawl scope is not constrained. <br>
Mitigation: Prefer explicit /kb add commands, keep same-origin crawling enabled, and set crawl depth, page, concurrency, and delay limits. <br>


## Reference(s): <br>
- [RagClaw Knowledge Base on ClawHub](https://clawhub.ai/emdzej/ragclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown and command output, with JSON available for search results when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite knowledge bases and local embedding models; output depends on the invoked /kb command.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
