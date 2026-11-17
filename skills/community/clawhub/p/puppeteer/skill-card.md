## Description:

Automate Chrome and Chromium with Puppeteer for scraping, testing, screenshots, and browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide Puppeteer browser automation for scraping, end-to-end testing, screenshots, PDF generation, and repeatable Chrome or Chromium workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to silently save workflow details, which could capture private sites, selectors, credentials, cookies, or authentication-flow details.

Mitigation: Require explicit user consent before writing memory files and avoid storing private sites, credentials, cookies, selectors, or authentication details.

Risk: The skill includes guidance for avoiding automation detection.

Mitigation: Remove or ignore anti-detection guidance and use Puppeteer only in compliance with site terms, rate limits, and authorization.

Risk: The skill may install npm dependencies without a reviewed lockfile.

Mitigation: Pin npm dependencies or install from a reviewed lockfile where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/puppeteer)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Skill homepage](https://clawic.com/skills/puppeteer)
- [Setup guide](setup.md)
- [Selectors guide](selectors.md)
- [Waiting patterns](waiting.md)
- [Memory template](memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local Puppeteer scripts, screenshots, PDFs, scraped data, and a local memory file under the user's Puppeteer workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
