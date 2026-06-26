## Description: <br>
This skill helps an agent convert Chinese natural-language search requests into structured JSON, call the Zeelin search API, and present search results or errors in a user-friendly format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urhd528](https://clawhub.ai/user/urhd528) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to query Zeelin search for public-opinion, news, review, trend, and related media data from Chinese natural-language prompts. It guides API key setup, builds the required request, calls the configured API endpoint, shows summarized results, and saves the full JSON response locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and search queries may be sent to a plain-HTTP Zeelin endpoint. <br>
Mitigation: Use the skill only with a trusted Zeelin endpoint, switch the configured API URL to HTTPS if supported, and verify the endpoint before entering an API key. <br>
Risk: Full search results are automatically saved as local JSON files and may contain sensitive topics or identifiers. <br>
Mitigation: Review saved result files after use and delete them when searches include sensitive or regulated information. <br>
Risk: Broad trigger phrases can cause the skill to run for general public-opinion, news, review, or trend requests. <br>
Mitigation: Confirm that the user intends to use Zeelin search before sending queries outside the environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/urhd528/zeelin-search-gsdata-es-bigdata) <br>
- [Natural language to JSON module](references/nl2json.md) <br>
- [Zeelin search API module](references/zenlin_search_api.md) <br>
- [Configured Zeelin website](http://search-skill.zeelin.cn) <br>
- [Configured Zeelin search API endpoint](http://search-skill.zeelin.cn:5000/api/es/search/natural) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, configuration guidance] <br>
**Output Format:** [Markdown summary with structured JSON files for saved search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows the first search results in the conversation and saves the complete API response as zeelin_search_results_YYYYMMDD_HHMMSS.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
