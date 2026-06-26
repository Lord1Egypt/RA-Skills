## Description: <br>
Use Valyu (valyu.ai) to search the web, extract content from web pages, answer with sources, and do deepresearch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unicodeveloper](https://clawhub.ai/user/unicodeveloper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Valyu-powered web, news, academic, financial, patent, and content extraction workflows with sources. It supports quick searches, URL content extraction, grounded answers, and longer DeepResearch reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries, URLs, research prompts, and optional files to Valyu. <br>
Mitigation: Use only inputs approved for Valyu processing and avoid sending sensitive or regulated data unless permitted by policy. <br>
Risk: The setup flow can ask for a Valyu API key in chat and save it in plaintext at ~/.valyu/config.json. <br>
Mitigation: Prefer VALYU_API_KEY from the environment or a secret manager, avoid pasting keys into chat, and avoid the setup command unless plaintext local storage is acceptable. <br>
Risk: Search, medical, financial, patent, and research outputs may be incomplete, stale, or misleading. <br>
Mitigation: Review cited sources and authoritative references before using outputs for high-stakes decisions. <br>


## Reference(s): <br>
- [Valyu Docs](https://docs.valyu.ai) <br>
- [Search API Reference](https://docs.valyu.ai/api-reference/endpoint/search) <br>
- [Contents API Reference](https://docs.valyu.ai/api-reference/endpoint/contents) <br>
- [Answer API Reference](https://docs.valyu.ai/api-reference/endpoint/answer) <br>
- [DeepResearch Guide](https://docs.valyu.ai/guides/deepresearch) <br>
- [ClawHub Skill Page](https://clawhub.ai/unicodeveloper/valyu-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and shell commands; runtime commands return JSON containing search results, extracted content, answers, citations, task status, and cost metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and VALYU_API_KEY; DeepResearch can return markdown and PDF URLs depending on requested output formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
