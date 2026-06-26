## Description: <br>
ZeeLin Search 智灵搜索 converts Chinese natural-language public-opinion and news queries into Zeelin search API requests, then presents results or errors in a human-readable format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urhd528](https://clawhub.ai/user/urhd528) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to query Zeelin for news, public-opinion, sentiment, and trend data from natural-language Chinese prompts. The skill is suited for retrieving and summarizing Zeelin API results after the user configures a Zeelin API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the Zeelin API. <br>
Mitigation: Use the skill only with a trusted Zeelin service account and avoid sensitive searches unless that data sharing is appropriate. <br>
Risk: The Zeelin API key is a secret used for signed requests. <br>
Mitigation: Store Zeelin_Api_Key securely, avoid exposing it in conversation output or logs, and rotate it if disclosure is suspected. <br>
Risk: Full search results may be saved locally as JSON files. <br>
Mitigation: Delete or protect generated zeelin_search_results JSON files when result contents are sensitive. <br>
Risk: The skill can activate on broad news, trend, or public-opinion prompts. <br>
Mitigation: Confirm user intent before sending ambiguous or sensitive broad queries to Zeelin. <br>


## Reference(s): <br>
- [ZeeLin Search 智灵搜索 release page](https://clawhub.ai/urhd528/zeelin-search-pro) <br>
- [Zeelin service website](https://skills.zeelin.cn) <br>
- [Natural language to JSON reference](references/nl2json.md) <br>
- [Zeelin search API reference](references/zenlin_search_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, configuration guidance] <br>
**Output Format:** [Markdown response with JSON request parameters, summarized API results, and a generated JSON results file when the Zeelin API call succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured Zeelin API key for signed requests and may write full search results to a local JSON file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
