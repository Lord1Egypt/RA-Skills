## Description: <br>
Public Apis Search helps agents search a local public API catalog by keyword, category, authentication type, HTTPS support, or random discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jijinbao-code](https://clawhub.ai/user/jijinbao-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover public APIs from a bundled local catalog, compare basic API metadata, and identify candidate provider documentation before integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may include plain-HTTP or third-party provider URLs. <br>
Mitigation: Prefer the HTTPS filter, verify provider documentation before use, and do not send credentials or sensitive data to plain-HTTP endpoints. <br>
Risk: Catalog entries are leads rather than endorsements of provider security, reliability, or terms. <br>
Mitigation: Review each provider's current documentation, authentication requirements, and terms before integrating an API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jijinbao-code/public-apis-search) <br>
- [public-apis source repository](https://github.com/public-apis/public-apis) <br>
- [public-apis README data source](https://raw.githubusercontent.com/public-apis/public-apis/master/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text API search results with names, descriptions, categories, authentication metadata, HTTPS/CORS indicators, and URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are limited by the CLI limit argument and may be filtered by category, authentication type, and HTTPS support.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
