## Description: <br>
Structured extraction and cleanup for public, user-authorized web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use Scraper to fetch public or user-authorized pages, extract readable text, and save local outputs for later summarization, analysis, or transformation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can fetch URLs provided by the user and keep extracted content locally. <br>
Mitigation: Use only public or explicitly authorized pages, and delete the local scraper output directory when saved content is no longer needed. <br>
Risk: Scraping can be misused to bypass access controls, robots restrictions, captchas, paywalls, or rate limits. <br>
Mitigation: Review target permissions before use and do not use the skill to bypass logins, paywalls, captchas, robots restrictions, access controls, or rate limits. <br>
Risk: Saved page text may include sensitive or unwanted content from the fetched page. <br>
Mitigation: Avoid collecting credentials or sensitive data, inspect saved outputs before reuse, and remove local files that should not be retained. <br>


## Reference(s): <br>
- [Scraper Safety](references/safety.md) <br>
- [ClawHub Scraper Listing](https://clawhub.ai/AGIstack/scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text, local text files, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves outputs locally under ~/.openclaw/workspace/memory/scraper/ and can print fetched or extracted page content previews.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
