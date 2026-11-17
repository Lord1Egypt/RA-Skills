## Description:

Use this skill when you need to take website screenshots with ScreenshotOne using direct curl commands, save the result to a local file, or choose ScreenshotOne API options such as full_page, viewport, wait, image, PDF, blocking, request, metadata, or storage settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[screenshotone](https://clawhub.ai/user/screenshotone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build visible curl requests for capturing website screenshots through ScreenshotOne's HTTP API, including full-page, viewport, timing, cleanup, request-context, metadata, and storage options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot requests can send private page content, cookies, headers, authorization data, and request context to ScreenshotOne.

Mitigation: Use the skill only for public or approved targets by default, and avoid production cookies, authorization headers, custom headers, and internal URLs.

Risk: Captured content may be delivered to ScreenshotOne or a configured storage bucket.

Mitigation: Treat ScreenshotOne and any configured storage bucket as recipients of the captured content before including sensitive pages or metadata.

Risk: Implicit invocation can trigger screenshot capture in environments that handle sensitive sites.

Mitigation: Disable implicit invocation or require explicit confirmation when operating in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/screenshotone/skills/screenshotone-render-website-screenshot)
- [ScreenshotOne Options Reference](references/screenshotone-options.md)
- [ScreenshotOne Options Documentation](https://screenshotone.com/docs/options/)
- [ScreenshotOne Access Key Dashboard](https://dash.screenshotone.com/access)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SCREENSHOTONE_ACCESS_KEY; generated commands may save image, PDF, HTML, Markdown, JSON, or storage-backed screenshot results depending on selected ScreenshotOne options.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
