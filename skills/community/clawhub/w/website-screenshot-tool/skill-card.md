## Description:

Automates website screenshots with responsive capture, batch processing, scheduled monitoring, visual comparison, and JSON history export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and site operators use this skill to capture webpages at common viewport sizes, compare page versions, schedule recurring captures, and export screenshot history for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may load untrusted, private, localhost, cloud metadata, or internal-network URLs.

Mitigation: Run captures in an isolated environment and restrict jobs to approved public URLs.

Risk: Screenshots and exported history can contain sensitive page content or browsing targets.

Mitigation: Write outputs only to a dedicated directory and protect or delete generated screenshots and JSON exports according to data-handling requirements.

Risk: The Selenium fallback uses a no-sandbox browser option that is not appropriate for untrusted sites.

Mitigation: Disable or remove the no-sandbox fallback before using the skill with untrusted websites.

Risk: Unpinned browser automation dependencies may change behavior over time.

Mitigation: Pin Python dependencies and browser versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/website-screenshot-tool)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG screenshots, JSON history data, and Markdown or code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot behavior depends on Playwright or Selenium browser automation and caller-provided URLs, viewport sizes, delays, and output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
