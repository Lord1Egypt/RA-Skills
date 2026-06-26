## Description: <br>
ZoomEye cyberspace search CLI guidance for finding internet assets, querying ZoomEye data, building ZoomEye dork queries, and supporting security research workflows such as asset mapping, exposure discovery, and vulnerability impact assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjbondone](https://clawhub.ai/user/jjbondone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and authorized researchers use this skill to translate asset-search goals into ZoomEye dork syntax and run ZoomEye CLI searches for internet-exposed hosts, services, web applications, certificates, and related metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ZoomEye API key and may store ZoomEye credentials locally through the ZoomEye CLI. <br>
Mitigation: Initialize ZoomEye credentials outside chat when possible, use a platform secret mechanism for automation, and rotate the key if it has been shared. <br>
Risk: ZoomEye searches can consume account quota and may reveal internet-exposed assets that require authorized handling. <br>
Mitigation: Use small page sizes and facets to validate searches before exporting larger result sets, and run searches only for authorized security or asset-management purposes. <br>


## Reference(s): <br>
- [ZoomEye Documentation](https://www.zoomeye.org/doc/) <br>
- [ZoomEye Profile and API Key Page](https://www.zoomeye.org/profile) <br>
- [ClawHub Skill Page](https://clawhub.ai/jjbondone/zoomeye-org-search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and ZoomEye dork query strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI setup steps, API-key initialization guidance, quota-aware search strategy, and search-result interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
