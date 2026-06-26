## Description: <br>
Extract clean article content from URLs through the AISA Tavily extract endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to extract readable article content from known URLs for summarization, comparison, or evidence review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled runtime includes broader search, research, and synthesis commands beyond URL extraction, and those commands send user inputs to AISA APIs. <br>
Mitigation: Review the selected CLI command before execution and use the skill only with information you intend to send to AISA. <br>
Risk: The skill requires the AISA_API_KEY credential. <br>
Mitigation: Provide the key through the environment, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Private URLs, sensitive queries, or confidential research material may be sent to AISA services. <br>
Mitigation: Use public or approved content unless you trust AISA with the material and have permission to process it through that service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/tavily-extract-aisa) <br>
- [AISA API Base URL](https://api.aisa.one/apis/v1) <br>
- [AISA API Key Site](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; extract output prints up to 3000 characters of raw content per URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
