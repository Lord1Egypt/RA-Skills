## Description: <br>
Auto-discover and use Web Skills Protocol (WSP) skills when interacting with websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xtresser](https://clawhub.ai/user/0xtresser) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to discover website-published WSP skills, select the relevant skill for a web task, and follow documented site workflows before falling back to scraping or UI automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website-hosted WSP instructions may direct authenticated or state-changing actions. <br>
Mitigation: Require explicit user confirmation before purchases, deployments, account changes, data deletion, or other high-impact API calls. <br>
Risk: Fetched skill files may come from untrusted or changed website content. <br>
Mitigation: Prefer a registry version or pinned commit, and review fetched skill files before use. <br>
Risk: Credentials could be requested for a site workflow. <br>
Mitigation: Provide credentials only to trusted domains and only after the user consents to the requested authentication method. <br>


## Reference(s): <br>
- [Web Skills Protocol specification](artifact/SPEC.md) <br>
- [Web Skills Protocol README](artifact/README.md) <br>
- [ClawHub release page](https://clawhub.ai/0xtresser/web-skills-protocol) <br>
- [Web Skills Protocol repository](https://github.com/0xtresser/Web-Skills-Protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text guidance with URLs, HTTP requests, parsed skill metadata, and structured results when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user consent for credentials and explicit confirmation before high-impact actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
