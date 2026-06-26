## Description: <br>
Give your agent web intelligence - screenshot any URL, extract structured page data, detect page changes, and analyze websites via the SnapAPI REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Boehner](https://clawhub.ai/user/Boehner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to call SnapAPI for screenshots, metadata extraction, page analysis, HTML rendering, PDF generation, batch URL processing, usage checks, and page-change monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected URLs, HTML, screenshots, and extracted page data to SnapAPI under the user's API key. <br>
Mitigation: Use it only for pages approved for third-party processing, and avoid sensitive internal pages unless that processing is explicitly approved. <br>
Risk: Page monitors can create recurring requests and webhook notifications for tracked URLs. <br>
Mitigation: Create monitors only with clear URL, interval, webhook, and stop expectations. <br>


## Reference(s): <br>
- [SnapAPI documentation](https://snapapi.tech/docs) <br>
- [SnapAPI website](https://snapapi.tech) <br>
- [ClawHub skill page](https://clawhub.ai/Boehner/snapapi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON, files] <br>
**Output Format:** [Markdown guidance with curl examples, JSON responses, and screenshot or PDF file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SNAPAPI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
