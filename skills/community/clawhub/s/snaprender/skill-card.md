## Description: <br>
SnapRender helps agents capture screenshots of URLs, HTML, or Markdown as image files, with options for device emulation, dark mode, full-page capture, and ad or cookie-banner blocking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[user0856](https://clawhub.ai/user/user0856) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use SnapRender to inspect web pages and rendered HTML or Markdown visually by generating screenshot files and response metadata through the SnapRender service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, HTML, Markdown, and signed screenshot links are sent to an external third-party screenshot service. <br>
Mitigation: Use the skill for public or non-sensitive pages by default, redact private HTML or Markdown before rendering, and create signed URLs only when link sharing is intended until expiration. <br>
Risk: The skill requires a sensitive SNAPRENDER_API_KEY credential. <br>
Mitigation: Use the preconfigured environment variable as documented and avoid exposing the API key in prompts, command output, or generated artifacts. <br>


## Reference(s): <br>
- [SnapRender ClawHub listing](https://clawhub.ai/user0856/snaprender) <br>
- [SnapRender signup](https://snap-render.com/auth/signup) <br>
- [SnapRender screenshot API](https://app.snap-render.com/v1/screenshot) <br>
- [SnapRender signed URL API](https://app.snap-render.com/v1/screenshot/sign) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, json metadata, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, saved screenshot files, and JSON response metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and SNAPRENDER_API_KEY; examples save screenshots and response metadata under /tmp.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
