## Description: <br>
Command-line helper for searching global network assets with ZoomEye AI, including advanced queries for asset discovery, CVE correlation, and bug bounty research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjbondone](https://clawhub.ai/user/jjbondone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers, developers, and bug bounty teams use this skill to convert natural-language asset discovery goals into ZoomEye AI dork queries and CLI commands. It supports CVE impact checks, new or changed asset monitoring, and scoped searches across services, geographies, organizations, and bug bounty sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ZoomEye API key and the security summary says the artifact asks users to paste that key into chat. <br>
Mitigation: Configure the API key locally through the CLI or a secret/environment mechanism, do not paste it into chat, and rotate the key if it was exposed. <br>
Risk: ZoomEye searches can consume account quota or run broad asset queries. <br>
Mitigation: Confirm intended scope before execution and start with small pages or facet probes before larger searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jjbondone/zoomeye-ai-search) <br>
- [Publisher profile](https://clawhub.ai/user/jjbondone) <br>
- [ZoomEye AI](https://www.zoomeye.ai) <br>
- [ZoomEye AI profile and API key page](https://www.zoomeye.ai/profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline dork syntax and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ZoomEye query strings, CLI setup steps, quota-aware search workflows, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
