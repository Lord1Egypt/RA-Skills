## Description: <br>
Generates XML sitemaps by crawling websites or scanning local files, with optional JSON, text, and robots.txt output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO practitioners use this skill to create sitemap.xml and robots.txt files for web projects from a live crawl or local source tree. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTPS verification is weakened during website crawling. <br>
Mitigation: Avoid relying on HTTPS crawl results on untrusted networks unless TLS verification is fixed. <br>
Risk: The skill can scan a user-specified local directory and write sitemap or robots files. <br>
Mitigation: Avoid sensitive local directories and review generated files before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/xml-sitemap-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [XML, JSON, plain text, and generated sitemap.xml or robots.txt files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports live same-domain crawling, local file scanning, configurable page limits and timeouts, and optional file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
