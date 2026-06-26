## Description: <br>
Automate Chrome and Chromium with Puppeteer for scraping, testing, screenshots, and browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1215656](https://clawhub.ai/user/1215656) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide Puppeteer-based browser automation for scraping, testing, screenshots, PDF generation, and repetitive Chrome or Chromium workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to create or update hidden local memory in ~/puppeteer/memory.md. <br>
Mitigation: Require explicit approval before creating or updating local memory, and review stored site, selector, and workflow notes. <br>
Risk: The skill includes bot-detection avoidance guidance for browser automation. <br>
Mitigation: Automate only sites or applications where the user has permission, respect rate limits and terms, and supervise scraping behavior. <br>
Risk: The skill may lead an agent to install npm packages or save executable Puppeteer scripts. <br>
Mitigation: Approve npm install commands directly and review generated scripts before saving or running them. <br>
Risk: Persistent browser profiles can retain cookies, sessions, or other local browsing data. <br>
Mitigation: Use a dedicated browser profile for automation and avoid storing credentials in scripts or shared profile data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1215656/puppeteer-1-0-0) <br>
- [Puppeteer skill homepage](https://clawic.com/skills/puppeteer) <br>
- [Setup guide](artifact/setup.md) <br>
- [Selectors guide](artifact/selectors.md) <br>
- [Waiting patterns](artifact/waiting.md) <br>
- [Memory template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Puppeteer script templates, setup commands, selector and waiting guidance, and local workflow notes when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
