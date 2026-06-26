## Description: <br>
Queries VirusTotal for a user-provided MD5 or SHA-256 hash and formats detection statistics, family labels, behavior, community notes, and key sample details. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[lingggao](https://clawhub.ai/user/lingggao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers and analysts use this skill to look up VirusTotal sample reports from hashes and produce concise Chinese-language reports for investigation notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VirusTotal hash lookups can disclose investigated sample identifiers to VirusTotal. <br>
Mitigation: Use the skill only when that disclosure is acceptable, and check organizational policy before enterprise or high-volume workflows. <br>
Risk: VirusTotal API keys can be exposed if reused broadly or handled outside the intended query flow. <br>
Mitigation: Prefer a limited, revocable official VirusTotal API key, provide it only for the current query, and do not store it after the report is produced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingggao/vt-insight) <br>
- [VirusTotal API v3 overview](https://docs.virustotal.com/reference/overview) <br>
- [VirusTotal get a file report](https://docs.virustotal.com/reference/file-info) <br>
- [VirusTotal get comments on a file](https://docs.virustotal.com/reference/files-comments-get) <br>
- [VirusTotal behavior reports summary](https://docs.virustotal.com/reference/file-all-behaviours-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language report with fixed sections for detection statistics, family assessment, research notes, and summary.] <br>

## Skill Version(s): <br>
1.8.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
