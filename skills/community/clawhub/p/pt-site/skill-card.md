## Description: <br>
Search and download torrents from NexusPHP-based PT sites, then add to qBittorrent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengqi](https://clawhub.ai/user/fengqi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Private tracker users and agents use this skill to search NexusPHP-based torrent sites, present torrent metadata, download selected torrent files, and add them to qBittorrent after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on private tracker cookies and may expose account credentials or passkeys if they are printed, logged, or shared in agent output. <br>
Mitigation: Store the cookie file with restrictive permissions, use only accounts approved for agent access, and redact cookies and passkeys from all outputs. <br>
Risk: The workflow can download torrent files and add them to qBittorrent. <br>
Mitigation: Require explicit user confirmation before any torrent is downloaded or added to qBittorrent. <br>
Risk: Automated tracker searches and downloads can violate site rules if requests are excessive or unauthorized. <br>
Mitigation: Use only authorized tracker accounts and keep request volume within the site's published rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengqi/pt-site) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and torrent result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include private tracker URLs, torrent metadata, and qBittorrent add instructions; secrets should be redacted from outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
