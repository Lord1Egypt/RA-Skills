## Description: <br>
Performs Google web searches using the Serper API and returns structured search results when provided a valid Serper API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OakcoderX](https://clawhub.ai/user/OakcoderX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run web searches through Serper when a user requests Google-style search results and a valid Serper API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to a third-party Serper API. <br>
Mitigation: Avoid searching for secrets, sensitive personal data, or internal-only project details. <br>
Risk: The skill requires a Serper API key and examples include inline key usage. <br>
Mitigation: Prefer setting SERPER_API_KEY as an environment variable instead of pasting keys directly into commands. <br>


## Reference(s): <br>
- [Serper website](https://serper.dev) <br>
- [Serper Google Search API endpoint](https://google.serper.dev/search) <br>
- [ClawHub skill page](https://clawhub.ai/OakcoderX/serper-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SERPER_API_KEY; search requests are sent to Serper and responses include organic results, search parameters, and credit usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
