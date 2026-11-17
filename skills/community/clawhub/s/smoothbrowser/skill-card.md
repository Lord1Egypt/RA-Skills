## Description:

SmoothBrowser helps agents use Smooth CLI to navigate websites, authenticate, scrape data, test web apps, fill forms, upload files, extract structured data, and automate browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniocirclemind](https://clawhub.ai/user/antoniocirclemind)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to drive browser sessions through Smooth CLI for web automation, authenticated workflows, form filling, web testing, and structured data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate actions in logged-in browser sessions and may act broadly across websites.

Mitigation: Use isolated sessions, restrict scope with --allowed-urls, and supervise authenticated or high-impact actions before execution.

Risk: Browser profiles can persist cookies and session state after automation completes.

Mitigation: Use --profile-read-only where possible, keep profile IDs purpose-specific, and delete profiles when they are no longer needed.

Risk: Uploaded files and browser session activity are sent through the Smooth CLI service.

Mitigation: Use the skill only when Smooth CLI is trusted for the data involved, upload only necessary files, and delete files after use.

Risk: The skill depends on an external CLI package and configured API key.

Mitigation: Verify or pin the Smooth CLI package version and keep API key configuration limited to the intended environment.

## Reference(s):

- [SmoothBrowser ClawHub release page](https://clawhub.ai/antoniocirclemind/skills/smoothbrowser)
- [Smooth account and API key portal](https://app.smooth.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to request JSON output from Smooth CLI or use response schemas for structured extraction.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
