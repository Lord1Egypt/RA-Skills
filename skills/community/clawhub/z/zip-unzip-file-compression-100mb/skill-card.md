## Description: <br>
Zip / Unzip - File Compression < 100MB compresses and decompresses ZIP or GZIP archives between 10MB and 100MB, storing outputs in AgentPMT cloud storage with signed download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to package large datasets, media collections, logs, backups, software distributions, or database exports as ZIP or GZIP archives, and to extract large archives for downstream processing. It is intended for non-sensitive archive workflows that can use AgentPMT-hosted cloud storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archives and extracted files are uploaded to AgentPMT cloud services and stored for signed URL retrieval. <br>
Mitigation: Use the skill only for non-sensitive archives unless the organization has approved AgentPMT storage, access, retention, and deletion practices. <br>
Risk: Inputs may include secrets, customer data, regulated records, proprietary files, or other material that must remain local. <br>
Mitigation: Do not submit sensitive or regulated content to this skill; keep inputs scoped to the minimum non-sensitive files needed for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/zip-unzip-file-compression-100mb) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/zip-unzip-file-compression-100mb) <br>
- [Generated Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, shell commands] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote tool returns JSON that can include file IDs, signed URLs, expiration information, file counts, and byte sizes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
