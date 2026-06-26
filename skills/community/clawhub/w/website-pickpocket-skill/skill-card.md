## Description: <br>
Website Pickpocket helps agents clone website pages into offline static copies or framework projects with localized resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenyangze](https://clawhub.ai/user/zhenyangze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to capture authorized website pages, localize their resources, and produce offline HTML or framework-specific project outputs for backup, migration, or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support copying websites without adequate authorization. <br>
Mitigation: Use it only on sites the user owns or is explicitly allowed to copy, and avoid anti-scraping workarounds unless authorized. <br>
Risk: Authenticated crawling can expose cookies, localStorage, or other session material. <br>
Mitigation: Treat cookies and localStorage values as credentials and avoid sharing generated outputs that contain sensitive session-derived content. <br>
Risk: Broad crawl settings can capture more pages or resources than intended. <br>
Mitigation: Keep crawl depth, page limits, and concurrency conservative, especially for unfamiliar sites. <br>
Risk: Generated JavaScript and downloaded resources may contain unsafe or unsuitable content. <br>
Mitigation: Review generated JavaScript and downloaded assets before publishing, running, or redistributing the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhenyangze/website-pickpocket-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown with inline shell commands, YAML configuration examples, and generated project file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide crawling, resource localization, and framework-specific project generation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
