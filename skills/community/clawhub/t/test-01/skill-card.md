## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Baidu web searches for live information, documentation, and research topics through a configured BAIDU_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided search queries to Baidu. <br>
Mitigation: Avoid submitting secrets, private documents, regulated data, confidential research terms, or other sensitive information as search queries. <br>
Risk: The BAIDU_API_KEY is required for API access. <br>
Mitigation: Provide the key only through the environment and treat it as sensitive credential material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ide-rea/test-01) <br>
- [Baidu AI Search web_search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON search results printed by a Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, count, and freshness parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
