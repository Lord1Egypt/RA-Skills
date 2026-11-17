## Description:

Automate Chrome and Chromium with Puppeteer for scraping, testing, screenshots, PDF generation, and browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1215656](https://clawhub.ai/user/1215656)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to create and troubleshoot Puppeteer workflows for scraping, end-to-end testing, screenshots, PDFs, and repetitive Chrome or Chromium browser tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep a local record of sites, selectors, and auth workflow patterns.

Mitigation: Inspect or disable ~/puppeteer/memory.md when retained workflow history is not desired, and avoid storing credentials or secrets in scripts or memory files.

Risk: Anti-detection guidance could conflict with website rules or authorization boundaries.

Mitigation: Use the skill only for permitted automation and review target-site terms, authorization, and rate-limit expectations before running scripts.

Risk: Generated browser automation can collect scraped data or operate in authenticated sessions.

Mitigation: Review scripts before execution, keep collected data local unless intentionally exported, and scope browser profiles and output directories to the intended workflow.

## Reference(s):

- [ClawHub Puppeteer Release](https://clawhub.ai/1215656/skills/puppeteer-1-0-0)
- [Puppeteer Skill Homepage](https://clawic.com/skills/puppeteer)
- [Setup Guide](artifact/setup.md)
- [Selectors Guide](artifact/selectors.md)
- [Waiting Patterns](artifact/waiting.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JavaScript and shell code blocks; generated local scripts and browser output files when used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Puppeteer workflow files under ~/puppeteer/.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact frontmatter, and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
