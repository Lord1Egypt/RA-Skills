## Description: <br>
Web Automation Suite helps agents connect to Chrome over CDP, automate page actions, scrape page data, fill forms, capture screenshots, and run scheduled monitoring tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate authorized browser workflows, collect webpage data, fill forms, take screenshots, and schedule recurring monitoring jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes broad browser automation guidance that could be misused on websites or accounts the user is not authorized to automate. <br>
Mitigation: Use it only with sites, accounts, and workflows where automation is permitted, and review target terms, selectors, rate limits, and submitted data before running. <br>
Risk: The skill discusses reducing bot-detection signals, which can create policy and trust risks. <br>
Mitigation: Avoid stealth or bot-detection bypass settings unless the site owner has explicitly authorized that automation. <br>
Risk: Saved browser state, cookies, or session files can expose authenticated accounts if mishandled. <br>
Mitigation: Treat storageState and session files like passwords: restrict access, keep them out of version control, rotate or delete them when no longer needed, and avoid sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxie48892-jpg/web-automation-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include reusable Playwright helper code, browser automation workflows, and scheduled task patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
