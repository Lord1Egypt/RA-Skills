## Description:

根据用户提供的哈希值，查询 VirusTotal 样本信息并输出检测统计、家族标签、沙箱行为和关键研究信息报告。

This skill is for research and development only.

## Publisher:

[lingggao](https://clawhub.ai/user/lingggao)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers and analysts use this skill to query MD5 or SHA256 hashes in VirusTotal and turn detection, behavior, relations, and community signals into a concise Chinese investigation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VirusTotal lookups can disclose submitted malware hashes and investigation interest to VirusTotal.

Mitigation: Confirm the user is comfortable querying the hash before lookup and only submit hashes the user intentionally provides.

Risk: A VirusTotal API key could be exposed if reused, stored, or sent outside the intended lookup.

Mitigation: Use any API key only for the current VirusTotal query, do not store it locally or remotely, and do not send it to other services.

Risk: Browser-based fallback could introduce account, cookie, upload, or download exposure if used carelessly.

Mitigation: Use unauthenticated browsing without login cookies, avoid uploads and downloads, and do not install executables, extensions, drivers, or other tools for the lookup.

## Reference(s):

- [VirusTotal API v3 Overview](https://docs.virustotal.com/reference/overview)
- [VirusTotal Get a File Report](https://docs.virustotal.com/reference/file-info)
- [VirusTotal Get Comments on a File](https://docs.virustotal.com/reference/files-comments-get)
- [VirusTotal File Behaviours Summary](https://docs.virustotal.com/reference/file-all-behaviours-summary)
- [VirusTotal Get All Behavior Reports for a File](https://docs.virustotal.com/reference/get-all-behavior-reports-for-a-file)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MD5 or SHA256 hash; may temporarily use a user-supplied VirusTotal API key for lookup.]

## Skill Version(s):

1.8.6 (source: server release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
