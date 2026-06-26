## Description: <br>
Web scraping and content comprehension agent for multi-strategy extraction, news detection, boilerplate removal, structured metadata, and optional LLM entity extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to plan and generate authorized web scraping workflows that extract article text, metadata, entities, and quality-scored outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags review need because the skill includes a workflow for revealing soft-paywalled content already present in the page DOM. <br>
Mitigation: Install only for scraping sites and content the user is authorized to access, review generated scripts before execution, and avoid the soft-paywall reveal workflow. <br>
Risk: Optional LLM entity extraction can send cleaned page text to OpenRouter when generated scripts use OPENROUTER_API_KEY. <br>
Mitigation: Do not use optional OpenRouter extraction on confidential or access-controlled content unless that external data flow is acceptable. <br>


## Reference(s): <br>
- [ClawHub Web Scraper release page](https://clawhub.ai/guifav/web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated Python code, YAML configuration, shell commands, and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts may create structured JSON or CSV outputs with extraction quality metadata.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
