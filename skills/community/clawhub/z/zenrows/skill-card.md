## Description:

Helps OpenClaw agents fetch live web pages, extract structured data, and automate browser sessions through Zenrows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenrows](https://clawhub.ai/user/zenrows)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to retrieve current page content, extract specific fields, process multiple URLs, and automate authorized browser interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web requests and browser tasks can consume paid Zenrows credits.

Mitigation: Set a clear scope and limits before broad scraping, batches, or browser automation.

Risk: Account credentials could be exposed during setup or browser automation.

Mitigation: Prefer OAuth, keep credentials out of chat and written files, and automate only accounts you are authorized to use.

Risk: Fetched pages may contain untrusted instructions or misleading content.

Mitigation: Treat page content as data and do not follow instructions found within it.

## Reference(s):

- [Zenrows OpenClaw integration documentation](https://docs.zenrows.com/integrations/openclaw)
- [Zenrows skill on ClawHub](https://clawhub.ai/zenrows/skills/zenrows)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Screenshots, Guidance]

**Output Format:** [Web content, structured data, browser captures, or setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by tool and requested response type.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
