## Description: <br>
Analyze any webpage URL for SEO issues and get actionable recommendations, including checks for title tags, meta descriptions, headings, keyword density, image alt text, Open Graph metadata, canonical URL, and word count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site owners, and content teams use this skill to audit a webpage for common SEO issues and receive a plain text report with prioritized recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script makes a network request to the URL supplied by the user. <br>
Mitigation: Analyze public pages or pages intentionally selected for audit, and avoid sensitive internal URLs unless the script and environment have been reviewed. <br>
Risk: The skill runs a local shell script with standard Unix tools. <br>
Mitigation: Review the script before installation or execution in environments with sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/claudiodrusus/shelly-seo-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/claudiodrusus) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text SEO analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports findings and recommendations for a single provided URL or piped HTML input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
