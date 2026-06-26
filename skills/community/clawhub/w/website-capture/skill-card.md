## Description: <br>
Take website screenshots, capture full pages, generate PDFs, and handle desktop, mobile, dark mode, stealth mode, cookie banner blocking, and batch URLs via the Allscreenshots cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panilya](https://clawhub.ai/user/panilya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to capture website screenshots or PDFs through the Allscreenshots cloud API without running a local browser. It supports common capture variants such as full-page, viewport-only, mobile, dark mode, and URL, base64, or binary responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs, rendering requests, API keys, and generated screenshots are sent to the Allscreenshots service. <br>
Mitigation: Use the skill only for pages your organization permits to be processed by Allscreenshots; avoid confidential, internal, authenticated, or unauthorized pages unless approved. <br>
Risk: Stored screenshot URLs or generated files may contain rendered page content. <br>
Mitigation: Treat returned screenshot URLs, PDFs, images, base64 payloads, and raw files as sensitive when the captured page contains sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panilya/website-capture) <br>
- [Allscreenshots dashboard](https://dashboard.allscreenshots.com) <br>
- [Allscreenshots screenshots API endpoint](https://api.allscreenshots.com/v1/screenshots) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Files, Guidance] <br>
**Output Format:** [Markdown with bash commands, JSON response examples, and screenshot or PDF file, URL, or base64 outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and ALLSCREENSHOTS_API_KEY; target URLs, render requests, and generated screenshots are processed by Allscreenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
