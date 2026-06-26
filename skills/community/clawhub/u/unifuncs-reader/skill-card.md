## Description: <br>
Use UniFuncs Reader API to read web pages and documents such as PDF and Word and Excel and PPTX URL, with AI-powered content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinlic](https://clawhub.ai/user/vinlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable content from web pages and documents, including PDF, Word, Excel, and PPTX URLs. It supports markdown or text extraction, CSS selector filtering, link summaries, cache control, optional cookie forwarding, and topic-focused extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private URLs, confidential documents, and cookie values can be sent to UniFuncs during reading. <br>
Mitigation: Use the skill only with URLs and documents you intend to share with UniFuncs, and avoid --set-cookie for live session cookies or internal resources unless that access is intentional. <br>


## Reference(s): <br>
- [ClawHub UniFuncs Reader release page](https://clawhub.ai/vinlic/unifuncs-reader) <br>
- [UniFuncs account and API key page](https://unifuncs.com/account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text extracted from the requested URL; JSON may be returned for non-text API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIFUNCS_API_KEY. Extraction is capped at 1,000,000 characters by default and can include images, link summaries, source references, or topic-focused output depending on options.] <br>

## Skill Version(s): <br>
0.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
