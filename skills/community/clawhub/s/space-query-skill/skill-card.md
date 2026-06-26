## Description: <br>
Builds search queries for FOFA, Quake, ZoomEye, and Shodan to support authorized network asset discovery, attack-surface review, and CVE-oriented investigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, developers, and authorized defenders use this skill to turn asset-discovery goals into platform-specific search queries for FOFA, Quake, ZoomEye, and Shodan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Asset-discovery and vulnerability queries can be misused against systems the user is not authorized to assess. <br>
Mitigation: Use the skill only for systems you own or are explicitly authorized to evaluate. <br>
Risk: CVE and product identifiers can be platform-specific or stale, producing misleading search results. <br>
Mitigation: Verify CVE details and platform-specific product identifiers against official platform or vulnerability sources before relying on the query. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gandli/space-query-skill) <br>
- [FOFA](https://fofa.info) <br>
- [Quake](https://quake.360.net) <br>
- [ZoomEye](https://zoomeye.org) <br>
- [Shodan](https://shodan.io) <br>
- [FOFA Blog](https://en.fofa.info/blog) <br>
- [Quake Blog](https://quake.360.net/blog) <br>
- [Field Reference](resources/fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with platform-specific query strings, explanations, and suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FOFA, Quake, ZoomEye, and Shodan syntax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
