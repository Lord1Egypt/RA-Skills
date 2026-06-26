## Description: <br>
Cloud browser automation CLI for AI agents powered by Scrapeless for navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, and using proxy or anti-detection browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scrapelesshq](https://clawhub.ai/user/scrapelesshq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to direct an agent through Scrapeless cloud browser sessions for web interaction, scraping, screenshots, form workflows, and web app testing. It is intended for authorized browser automation workflows that require cloud execution, session management, or proxy-backed browser configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser automation, proxy, and anti-detection capabilities can be misused on sites where automation is not authorized. <br>
Mitigation: Use the skill only on websites the operator is authorized to automate, and avoid proxy or anti-detection options unless they are clearly permitted for the workflow. <br>
Risk: API keys, proxy credentials, cookies, localStorage values, screenshots, and live preview URLs can expose sensitive account or session data. <br>
Mitigation: Protect Scrapeless API keys and proxy credentials, treat browser outputs as sensitive secrets, and avoid running workflows on sensitive logged-in accounts without explicit need. <br>
Risk: Session recording can retain sensitive browser activity on Scrapeless-managed infrastructure. <br>
Mitigation: Keep recording disabled by default and enable it only for deliberate debugging or audit workflows where captured data is approved for storage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scrapelesshq/scrapeless-scraping-browser-skill) <br>
- [Authentication](references/authentication.md) <br>
- [Scrapeless Dashboard](https://app.scrapeless.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session IDs, element references, screenshots, cookies, localStorage values, extracted page data, and live preview URLs from browser automation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
