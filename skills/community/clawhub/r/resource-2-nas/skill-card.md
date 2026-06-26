## Description: <br>
Use when a user asks to search for movie, TV, animation, or other media resources; provides a Quark/Baidu share link to save; wants to verify saved resources through OpenList; wants to view/cancel OpenList transfer task progress; or wants to copy saved resources to NAS/SMB storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leochens](https://clawhub.ai/user/leochens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find Baidu or Quark media resource links, preview and save shared cloud-drive resources, verify saved content through OpenList, and copy selected resources into NAS/SMB-backed storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses cloud-drive cookies and an OpenList token that can grant broad account or storage access. <br>
Mitigation: Treat these values as full credentials, keep them out of commits and shared logs, and prefer a dedicated or low-privilege OpenList token where possible. <br>
Risk: Save, copy, cancel, raw_url download, and link-check actions can affect private links, cloud-drive state, or NAS-backed storage. <br>
Mitigation: Require explicit confirmation after a preview before running any mutating or private-link operation. <br>
Risk: Custom API bases or proxies can expose searches, links, or credentials to infrastructure the user does not control. <br>
Mitigation: Use only trusted API bases and proxies, and avoid routing credentialed operations through untrusted services. <br>


## Reference(s): <br>
- [Resource 2 NAS ClawHub Page](https://clawhub.ai/leochens/resource-2-nas) <br>
- [README](artifact/README.md) <br>
- [Sub-Agent Runbook](artifact/SUBAGENT.md) <br>
- [PanSou Public Endpoint](https://so.252035.xyz/) <br>
- [Configuration Guide](https://guantou.site/archives/N2CmhISt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise guidance, with JSON available from helper commands for agent workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are capped to the top 50 by default; save, copy, and cancel operations use preview-before-confirmation flows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
