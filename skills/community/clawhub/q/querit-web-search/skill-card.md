## Description: <br>
Advanced web search using the Querit API with support for site filtering, time ranges, geolocation, and language targeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MurphyZzzzz](https://clawhub.ai/user/MurphyZzzzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run real-time web searches through Querit, including searches constrained by sites, dates, countries, and languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, filters, and related request data are sent to Querit using the configured API key. <br>
Mitigation: Avoid including secrets, private documents, or sensitive personal information in queries unless sharing that information with Querit is acceptable. <br>
Risk: The skill depends on a configured Querit API key and the external Querit API. <br>
Mitigation: Install only when the user is comfortable providing a Querit API key and relying on Querit for search responses. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MurphyZzzzz/querit-web-search) <br>
- [Publisher profile](https://clawhub.ai/user/MurphyZzzzz) <br>
- [Querit homepage](https://querit.ai) <br>
- [Querit POST API reference](https://www.querit.ai/en/docs/reference/post) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON text from the Querit search API, or JSON-formatted error output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and QUERIT_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
