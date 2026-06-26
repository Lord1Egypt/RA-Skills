## Description: <br>
Research and score prospective web design clients. Crawl their site, assess fit, and produce a qualification report. Use when asked to qualify a lead, research a company, score a prospect, or check out a website. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelance web designers use this skill to research prospective clients, inspect public website evidence, score lead fit, and produce a saved qualification report with optional outreach support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public websites and can trigger optional Playwright and Chromium installation. <br>
Mitigation: Install only if public website fetching and the optional browser dependency are acceptable for the target environment. <br>
Risk: Lead reports may retain prospect contact details and business assessments on local disk. <br>
Mitigation: Use a private reports directory and delete old reports when the information should not persist. <br>
Risk: Broad natural-language triggers can cause the agent to start prospect research when the user provides a company or website. <br>
Mitigation: Confirm the intended target website before crawling, especially when only a company name or multiple candidates are available. <br>


## Reference(s): <br>
- [Edge Cases - Web Design Lead Qualifier](artifact/references/edge-cases.md) <br>
- [ClawHub skill page](https://clawhub.ai/99rebels/web-design-lead-qualifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, chat guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves local lead qualification reports and may produce chat-only email drafts and talking points.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
