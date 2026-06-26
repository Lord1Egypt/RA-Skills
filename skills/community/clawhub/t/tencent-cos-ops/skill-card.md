## Description: <br>
Tencent COS Ops helps agents upload, download, list, and delete files in Tencent Cloud COS buckets using configured COS credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrybit](https://clawhub.ai/user/henrybit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to let an agent manage Tencent Cloud COS objects for upload, download, listing, deletion, and month-based object organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete Tencent COS objects when supplied with valid COS credentials. <br>
Mitigation: Use a dedicated COS key restricted to the intended bucket and prefixes, avoid granting delete permission unless needed, verify object keys before deletion, and enable versioning or retention where possible. <br>
Risk: Downloads can overwrite important local files if destination paths are chosen carelessly. <br>
Mitigation: Choose download paths deliberately, prefer an isolated working directory, and review destination paths before running download commands. <br>


## Reference(s): <br>
- [Tencent COS API Reference](references/cos_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/henrybit/tencent-cos-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent COS credentials and bucket configuration before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md version table, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
