## Description: <br>
Organizes a messy local music library into a clean language, artist, and album hierarchy using acoustic fingerprinting, deduplication, metadata enrichment, and optional Spotify sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drajb](https://clawhub.ai/user/drajb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and music-library maintainers use this skill to set up, run, and monitor a local Sonic Phoenix pipeline that fingerprints tracks, detects duplicates, enriches tags, organizes files, and optionally syncs Spotify playlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly reorganize local music files. <br>
Mitigation: Back up the target music folder, set MUSIC_ROOT to the narrowest intended directory, and run dry-run or status checks before running the full pipeline. <br>
Risk: Optional Spotify sync uses account access and a locally cached token. <br>
Mitigation: Enable Spotify sync only when needed, keep credentials and token cache private, and review playlist backups before syncing. <br>
Risk: The security guidance flags eval-based path handling in status.sh. <br>
Mitigation: Treat status.sh cautiously until the path handling is fixed, and avoid untrusted configuration values or paths when running it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drajb/ultimate-music-manager) <br>
- [Project source declared in skill metadata](https://github.com/drajb/sonic-phoenix) <br>
- [Data Files Reference](artifact/references/data-files.md) <br>
- [Language Hints Guide](artifact/references/language-hints-guide.md) <br>
- [Safety Guard Hook](artifact/hooks/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local environment variables, local filesystem paths, and optional OAuth setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
