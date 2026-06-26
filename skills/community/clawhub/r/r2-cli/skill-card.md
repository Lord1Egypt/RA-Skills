## Description: <br>
Minimal Python CLI for secure upload, download, list, and delete operations on Cloudflare R2 storage using AWS Signature V4 authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zororaka00](https://clawhub.ai/user/zororaka00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent prepare and run Cloudflare R2 object storage operations, including upload, download, listing, and deletion, from a minimal Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage objects in the configured Cloudflare R2 bucket, including destructive delete operations. <br>
Mitigation: Use a dedicated least-privilege R2 key and double-check upload and delete commands before running them. <br>
Risk: The skill depends on R2 credentials supplied through environment variables. <br>
Mitigation: Keep credentials out of source control, use a secret manager or temporary shell environment, and rotate keys regularly. <br>
Risk: The CLI depends on defusedxml for hardened XML parsing. <br>
Mitigation: Install defusedxml from a trusted package source before using list operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zororaka00/r2-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Cloudflare R2 environment variables and produces commands that may read, write, list, or delete bucket objects.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
