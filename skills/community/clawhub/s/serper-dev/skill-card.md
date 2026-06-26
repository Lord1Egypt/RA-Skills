## Description: <br>
Searches Google through the Serper.dev API and returns structured results for programmatic research, lead generation, and local business discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Serper.dev Google searches for lead generation, competitor research, content research, and local business discovery while returning structured results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search and Places queries are sent to Serper.dev. <br>
Mitigation: Do not use secrets, confidential business terms, regulated data, or personal information unless that third-party handling is acceptable. <br>
Risk: The skill requires a Serper API key in the agent environment. <br>
Mitigation: Protect SERPER_API_KEY and avoid exposing it in prompts, generated output, logs, or shared files. <br>
Risk: Places results can include business phone numbers and addresses. <br>
Mitigation: Handle returned contact and location data according to applicable privacy, marketing, and retention rules. <br>


## Reference(s): <br>
- [Serper Web Search endpoint](https://google.serper.dev/search) <br>
- [Serper News endpoint](https://google.serper.dev/news) <br>
- [Serper Images endpoint](https://google.serper.dev/images) <br>
- [Serper Places endpoint](https://google.serper.dev/places) <br>
- [Serper Shopping endpoint](https://google.serper.dev/shopping) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SERPER_API_KEY and sends intended search or Places queries to Serper.dev.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
