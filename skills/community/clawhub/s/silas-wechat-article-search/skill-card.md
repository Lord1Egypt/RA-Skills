## Description: <br>
Searches WeChat public-account articles through Sogou WeChat and Serper-backed sources, parses article text and images with Python, and guides scoring, deduplication, and Feishu knowledge-base ingestion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aohoyo](https://clawhub.ai/user/aohoyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and knowledge-base operators use this skill to find relevant WeChat articles, extract full article content, score usefulness, remove duplicates, and prepare selected material for Feishu documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes recurring WeChat article collection and Feishu knowledge-base writes with limited user-control safeguards. <br>
Mitigation: Review or disable the hourly cron unless needed, confirm destinations before writes, and keep a human review step before ingesting content. <br>
Risk: The workflow uses sensitive credentials and may send search terms to Sogou or Serper. <br>
Mitigation: Scope Feishu permissions narrowly, protect SERPER_API_KEY, and avoid sensitive internal search terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aohoyo/silas-wechat-article-search) <br>
- [Example output](references/example-output.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands, Python usage examples, and JSON article records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce parsed article JSON files and proposed Feishu knowledge-base entries when the agent follows the workflow.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
