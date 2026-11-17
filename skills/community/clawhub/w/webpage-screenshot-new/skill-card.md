## Description:

Captures and saves screenshots of specified web pages using Puppeteer or similar browser automation tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxx94666](https://clawhub.ai/user/wxx94666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to capture webpage screenshots for visual checks, documentation, or saved page evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may make network requests to untrusted, private, or internal URLs.

Mitigation: Run screenshots only for URLs the user is comfortable requesting, and avoid private or internal targets unless the environment is approved for that access.

Risk: Installing Puppeteer without a pinned version or lockfile can introduce dependency drift.

Mitigation: Use a pinned Puppeteer version with a lockfile before installing or deploying the skill.

Risk: Running a browser automation stack with broad privileges can increase impact if a page or dependency behaves unexpectedly.

Mitigation: Run Puppeteer in a low-privilege or isolated environment.

## Reference(s):

- [Puppeteer documentation](https://pptr.dev/)
- [ClawHub skill page](https://clawhub.ai/wxx94666/skills/webpage-screenshot-new)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and example browser automation code; screenshot files are created by the user's runtime environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
