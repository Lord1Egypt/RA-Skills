## Description: <br>
Qryma AI Search retrieves Web information and returns LLM-friendly data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qryma888](https://clawhub.ai/user/qryma888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Qryma web searches from an agent workflow and return search results as Markdown, Brave-like JSON, or raw API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries and the QRYMA_API_KEY to Qryma or to a configured custom endpoint. <br>
Mitigation: Use only the default Qryma endpoint or a custom endpoint you explicitly trust, and store the API key in a secure environment or dedicated config file. <br>
Risk: The script can read QRYMA_API_KEY and QRYMA_ENDPOINT from a local .env file in the current directory if the dedicated config file is absent. <br>
Mitigation: Run the skill from trusted directories and avoid directories containing untrusted .env files. <br>
Risk: Pasting a real API key into chat or logs can expose credentials. <br>
Mitigation: Configure QRYMA_API_KEY outside chat using environment variables or a protected local config file. <br>


## Reference(s): <br>
- [Qryma Search on ClawHub](https://clawhub.ai/qryma888/qryma-search) <br>
- [Qryma](https://qryma.com) <br>
- [Google Custom Search Interface Languages](https://developers.google.com/custom-search/docs/xml_results_appendices#interfaceLanguages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Brave-like JSON, or raw JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and QRYMA_API_KEY; supports max-results, language, safe search, mode, and output format options.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
