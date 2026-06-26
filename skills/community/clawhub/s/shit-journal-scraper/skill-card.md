## Description: <br>
Automates extraction and AI-assisted analysis of research papers from shitjournal.org, including titles, abstracts, DOI values, and publication dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Excalibur9527](https://clawhub.ai/user/Excalibur9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to collect publicly available Shit Journal article metadata and summarize abstracts for knowledge-management or analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses a target website and may send scraped page content to an AI service for analysis. <br>
Mitigation: Use it only on pages you are permitted to process, and avoid private, confidential, or consent-sensitive content unless the data-sharing path is approved. <br>
Risk: Headless browser automation and scraping can trigger site policy, availability, or network-control concerns. <br>
Mitigation: Review the target site's terms and run the skill in an environment with appropriate dependency review and network controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Excalibur9527/shit-journal-scraper) <br>
- [Shit Journal](https://shitjournal.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text with JSON-ready article records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs scraped article titles, abstracts, DOI values, and analysis-oriented summaries; requires network access to the target website and Playwright Chromium dependencies.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
