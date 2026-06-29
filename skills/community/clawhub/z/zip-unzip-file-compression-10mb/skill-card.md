## Description: <br>
Compresses and decompresses ZIP and GZIP archives under 10 MB through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to compress small files into ZIP/GZIP archives or extract uploaded archives in AgentPMT workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected archives and file contents are processed by AgentPMT as a remote service. <br>
Mitigation: Do not submit secrets, credentials, private keys, or confidential documents unless remote processing is acceptable. <br>
Risk: Stored outputs are available through cloud storage and signed URLs for 7 days by default. <br>
Mitigation: Use store_file: false and include_contents: true when inline results are sufficient, and avoid sharing signed URLs for sensitive files. <br>
Risk: ZIP and GZIP operations are limited to archives under 10 MB, with ZIP compression capped at 200 files. <br>
Mitigation: Validate input size and file count before calling the skill; use a larger archive workflow when those limits are exceeded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/zip-unzip-file-compression-10mb) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/zip-unzip-file-compression-10mb) <br>
- [Generated action schema](schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines remote compress and decompress calls that return JSON with file IDs, signed URLs, warnings, and optional base64 contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
