## Description: <br>
Uses Tavily AI for web search, deeper research, and URL content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devang668](https://clawhub.ai/user/devang668) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to search the web, run Tavily research tasks with citations, and extract readable content from URLs from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact bundles and automatically loads a Tavily API-key-like value from .env. <br>
Mitigation: Remove or replace the bundled .env value before installation and use a user-controlled Tavily API key. <br>
Risk: Queries, URLs, and extracted content are sent to Tavily's external service. <br>
Mitigation: Do not submit secrets, private or internal URLs, customer data, or regulated content unless the deployment has approved that data flow. <br>
Risk: Commands with --output can write files and may overwrite existing paths chosen by the user. <br>
Mitigation: Choose output paths deliberately and review generated content before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devang668/travily) <br>
- [Publisher Profile](https://clawhub.ai/user/devang668) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Extract API Endpoint](https://api.tavily.com/extract) <br>
- [Tavily Research API Endpoint](https://api.tavily.com/research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Console text, JSON responses, or saved Markdown/text files depending on command options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search supports result count, search depth, time range, domain filters, and raw content; research supports model selection and optional source limits; extract supports basic or deep extraction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
