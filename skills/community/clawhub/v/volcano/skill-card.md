## Description: <br>
Provides non-sensitive summaries of Volcano Engine public product information, pricing links, console-visible billing overviews, and service announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and account users use this skill to summarize Volcano Engine product specs, pricing references, billing trends visible in their own console, and service announcements without handling sensitive credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Console billing summaries may contain private account or cost information. <br>
Mitigation: Review billing output before sharing it and limit use to information the user is authorized to view. <br>
Risk: The skill could encounter credentials, secrets, or account identifiers while viewing console pages. <br>
Mitigation: Do not capture, store, or reproduce credentials, secrets, or account identifiers in summaries. <br>
Risk: Automated browsing can exceed platform expectations if repeated too aggressively. <br>
Mitigation: Respect Volcano Engine access limits and keep collection to visible, compliant, non-sensitive page content. <br>


## Reference(s): <br>
- [Volcano Engine homepage](https://www.volcengine.com/) <br>
- [Volcano Engine documentation](https://www.volcengine.com/docs) <br>
- [Volcano Engine console](https://console.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries with source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API calls; summarizes visible, non-sensitive information only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
