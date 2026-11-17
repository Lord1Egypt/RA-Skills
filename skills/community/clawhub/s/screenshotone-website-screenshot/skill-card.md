## Description:

Use this skill when you need to take website screenshots with ScreenshotOne using direct curl commands, save the result to a local file, or choose ScreenshotOne API options such as full_page, viewport, wait, image, PDF, blocking, request, metadata, or storage settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krasun](https://clawhub.ai/user/krasun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create visible curl commands for capturing web pages with ScreenshotOne, saving the result locally, and selecting screenshot, PDF, cleanup, timing, viewport, request, metadata, or storage options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, rendered page content, screenshots, API keys, and optional session credentials may be sent to ScreenshotOne.

Mitigation: Use only intentional target URLs, avoid cookies, authorization headers, private authenticated pages, or storage uploads unless that exposure is intended, keep SCREENSHOTONE_ACCESS_KEY in the environment, and invoke each capture explicitly.

## Reference(s):

- [ScreenshotOne Options Reference](references/screenshotone-options.md)
- [ScreenshotOne Screenshot Options](https://screenshotone.com/docs/options/)
- [ScreenshotOne API Endpoint](https://api.screenshotone.com/take)
- [ScreenshotOne Access Dashboard](https://dash.screenshotone.com/access)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use curl with URL-encoded ScreenshotOne API parameters and may write local image, PDF, HTML, or Markdown files depending on the selected format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
