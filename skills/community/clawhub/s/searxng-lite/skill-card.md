## Description: <br>
SearXNG-lite provides local, script-based multi-engine web search aggregation for agents across general web, developer, academic, knowledge, news, and other search categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrzhangkris](https://clawhub.ai/user/mrzhangkris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to run local Python-based searches across multiple web, code, academic, knowledge, discussion, model, and news sources when a task needs broader or engine-specific search coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries can be sent to selected providers and any configured proxy, which may expose sensitive terms or private URLs. <br>
Mitigation: Do not search for secrets, credentials, customer data, private internal URLs, or sensitive proprietary topics; only configure a proxy you trust. <br>
Risk: Python dependencies and runtime setup can affect the local agent environment. <br>
Mitigation: Install dependencies in a virtual environment when possible and review the dependency commands before running the search script. <br>
Risk: Search coverage can vary by enabled engines, proxy availability, provider blocking, or silent skips for proxy-required engines. <br>
Mitigation: Review the returned engines_used and errors fields, and configure only the engines and trusted proxy settings needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrzhangkris/searxng-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results by default, with optional compact human-readable text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include title, URL, content, source engines, score, result count, elapsed time, engines used, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
