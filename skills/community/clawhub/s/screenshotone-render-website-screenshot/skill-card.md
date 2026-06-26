## Description: <br>
Use this skill when you need to take website screenshots with ScreenshotOne using direct curl commands, save the result to a local file, or choose ScreenshotOne API options such as full_page, viewport, wait, image, PDF, blocking, request, metadata, or storage settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[screenshotone](https://clawhub.ai/user/screenshotone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate direct curl commands for ScreenshotOne's HTTP API, capture website screenshots, choose capture options, and save results to local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External screenshot requests may send target URLs, page content, cookies, authorization headers, or other context to ScreenshotOne. <br>
Mitigation: Use this skill only when ScreenshotOne is an intended external service, and avoid private internal URLs, session cookies, authorization headers, personal data, or confidential pages unless that disclosure is approved. <br>
Risk: Saved screenshots may contain sensitive page content. <br>
Mitigation: Use safe output filenames and handle generated image, PDF, HTML, or Markdown files according to the sensitivity of the captured page. <br>
Risk: Embedding the ScreenshotOne access key directly in commands can expose credentials. <br>
Mitigation: Pass the key through the SCREENSHOTONE_ACCESS_KEY environment variable and avoid pasting credential values into shared commands or documents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/screenshotone/screenshotone-render-website-screenshot) <br>
- [ScreenshotOne options reference](references/screenshotone-options.md) <br>
- [ScreenshotOne screenshot options documentation](https://screenshotone.com/docs/options/) <br>
- [ScreenshotOne](https://screenshotone.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl commands that call ScreenshotOne, pass options through URL-encoded parameters, and write screenshot or document outputs such as PNG, JPG, WebP, PDF, HTML, or Markdown to local files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
