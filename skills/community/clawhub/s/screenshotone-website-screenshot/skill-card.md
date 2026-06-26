## Description: <br>
Use this skill when you need to take website screenshots with ScreenshotOne using direct curl commands, save the result to a local file, or choose ScreenshotOne API options such as full_page, viewport, wait, image, PDF, blocking, request, metadata, or storage settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krasun](https://clawhub.ai/user/krasun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate ScreenshotOne curl commands for capturing website screenshots, PDFs, or related outputs with configurable viewport, timing, cleanup, request, metadata, and storage options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshot targets and request context can be routed through the external ScreenshotOne service. <br>
Mitigation: Use the skill only for approved public or non-sensitive pages unless there is explicit approval for the target content. <br>
Risk: Cookies, headers, authorization values, or other sensitive request data may be included in screenshot requests. <br>
Mitigation: Avoid sending production cookies, bearer tokens, API keys, sensitive headers, or regulated data in ScreenshotOne requests. <br>
Risk: The ScreenshotOne access key is required to execute generated commands. <br>
Mitigation: Pass the access key through the SCREENSHOTONE_ACCESS_KEY environment variable and avoid embedding it in shared command text or committed files. <br>


## Reference(s): <br>
- [ScreenshotOne Options Reference](references/screenshotone-options.md) <br>
- [ScreenshotOne Options Documentation](https://screenshotone.com/docs/options/) <br>
- [ClawHub Skill Page](https://clawhub.ai/krasun/screenshotone-website-screenshot) <br>
- [Publisher Profile](https://clawhub.ai/user/krasun) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl command templates and option-selection guidance; screenshot files are created only when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
