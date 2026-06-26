## Description: <br>
Super Search Engine helps agents construct public web search queries across 17 domestic and international engines, including advanced operators, time filters, privacy-oriented engines, DuckDuckGo bangs, and WolframAlpha queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to choose a suitable public search provider and compose search URLs for web research, site-specific searches, time-filtered searches, privacy-oriented searches, and knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are shared with the selected external search provider. <br>
Mitigation: Do not include secrets, credentials, internal hostnames, private incident details, personal data, or regulated information in search queries unless sharing with that provider is acceptable. <br>
Risk: Advanced search operators can be misused for unauthorized research. <br>
Mitigation: Use advanced operators only for legitimate, authorized research and follow applicable organizational policies. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls] <br>
**Output Format:** [Markdown with URL templates and JSON web_fetch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; queries are sent to the selected external search provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact documentation reports v2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
