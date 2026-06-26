## Description: <br>
Soushen is a Playwright-based Bing search skill that returns structured search results and can extract page elements such as links, forms, buttons, scripts, metadata, cookies, and text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexian2001](https://clawhub.ai/user/hexian2001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run Bing searches without an API key and to inspect public webpages for structured search results, page text, and page elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep browsing mode can collect sensitive page data, including cookies, form values, and page content. <br>
Mitigation: Restrict use to public, non-sensitive sites unless cookie output, form-value capture, and privacy warnings are explicitly gated by user consent. <br>
Risk: The browsing implementation weakens normal browser protections beyond what the stated search purpose requires. <br>
Mitigation: Review and narrow the browsing behavior before installation, remove or gate unsafe browser flags, and scope execution to approved domains. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code] <br>
**Output Format:** [JSON for CLI results and Markdown-style guidance for agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search mode returns result objects; deep mode can return page text, links, forms, buttons, scripts, metadata, and cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
