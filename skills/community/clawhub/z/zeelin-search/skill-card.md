## Description: <br>
ZeeLin Search helps an agent turn Chinese natural-language search requests into a Zeelin API query, call the Zeelin search API with configured credentials, and present the results with a saved JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingjiusheng](https://clawhub.ai/user/yingjiusheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query ZeeLin Search for public-opinion, news, trend, and related-report data from Chinese natural-language prompts. The agent checks for a configured Zeelin API key, sends a signed API request, summarizes the returned records, and writes the full JSON response locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zeelin API key and uses it to sign outbound requests. <br>
Mitigation: Use a revocable API key, keep it in configuration rather than chat, and rotate it if exposure is suspected. <br>
Risk: Search requests are sent to an external Zeelin endpoint and full result JSON files may be written locally. <br>
Mitigation: Avoid sensitive search terms, verify the configured endpoint before use, and review or remove saved result files according to local data handling requirements. <br>
Risk: Server security evidence notes inconsistent package identity metadata. <br>
Mitigation: Install only from the expected ClawHub publisher profile and verify the release slug and version before deployment. <br>


## Reference(s): <br>
- [Natural Language to JSON Module](artifact/references/nl2json.md) <br>
- [ZeeLin Search API Module](artifact/references/zenlin_search_api.md) <br>
- [ZeeLin Search Website](https://skills.zeelin.cn) <br>
- [ZeeLin Natural Search API Endpoint](https://skills.zeelin.cn/v2/api/es/search/natural) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, api calls, configuration guidance] <br>
**Output Format:** [Markdown response with structured JSON files saved locally] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful calls display a concise result summary and save the complete API response as zeelin_search_results_YYYYMMDD_HHMMSS.json in the user directory.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
