## Description:

Search and download torrents from NexusPHP-based PT sites, then add to qBittorrent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengqi](https://clawhub.ai/user/fengqi)

### License/Terms of Use:


## Use Case:

External users and developers use Pt Site to search NexusPHP-based private tracker sites, review torrent metadata, download selected .torrent files, and add them to qBittorrent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracker cookies and passkeys are sensitive credentials that may grant account access.

Mitigation: Treat cookies and passkeys as passwords, keep them out of logs and shared transcripts, and use redacted credential handling.

Risk: The skill can lead to torrent downloads and qBittorrent imports with limited safeguards.

Mitigation: Require final user confirmation before each download or qBittorrent import, and use only qBittorrent instances the user is comfortable letting an agent access.

Risk: Downloaded torrent files may be written to shared temporary storage.

Mitigation: Prefer a private temporary directory and unique filenames, then remove files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengqi/skills/pt-site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local tracker credentials, torrent files, and qBittorrent import steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
