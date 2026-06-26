## Description: <br>
Fetch and manage Read AI meeting data, including summaries, transcripts, action items, engagement metrics, meeting search, digests, and webhook setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandons7](https://clawhub.ai/user/brandons7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and engineers use this skill to retrieve, search, export, and receive Read AI meeting records and Limitless conversation lifelogs through API calls, local cache files, and a webhook receiver. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Read AI meeting records and Limitless conversation lifelogs that may contain sensitive transcripts, summaries, participants, decisions, and action items. <br>
Mitigation: Install only when this access is intended, use a least-privilege API key where available, and review the records before sharing outputs. <br>
Risk: The skill stores API keys, meeting data, lifelogs, webhook payloads, and logs on the local filesystem. <br>
Mitigation: Restrict permissions on ~/.config/readai and ~/.readai, rotate exposed keys, and regularly secure or delete cached data that is no longer needed. <br>
Risk: The optional AI summary mode can send conversation excerpts to the Claude CLI. <br>
Mitigation: Avoid the --ai option unless sending those excerpts to Claude is acceptable for the user's data handling requirements. <br>
Risk: The webhook receiver can expose incoming meeting payload handling if bound beyond localhost or deployed without external protection. <br>
Mitigation: Keep the receiver bound to localhost where possible, or place it behind appropriate network access controls and webhook protections. <br>


## Reference(s): <br>
- [Read AI API Reference](references/api-reference.md) <br>
- [Read AI API](https://api.read.ai/v1) <br>
- [Limitless API](https://api.limitless.ai/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/brandons7/readai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, shell command output, and local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local meeting, transcript, lifelog, digest, index, and webhook log files under user configuration and data directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
