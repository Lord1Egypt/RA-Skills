## Description: <br>
Voicenotes syncs voice recordings, transcripts, tags, and AI summaries from Voicenotes.com into an agent workspace and can export notes as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnhansen](https://clawhub.ai/user/shawnhansen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers who use Voicenotes use this skill to retrieve recordings, transcripts, tags, summaries, and action items from their account and sync them into local Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Voicenotes access token. <br>
Mitigation: Keep VOICENOTES_TOKEN out of commits, logs, screenshots, and shared shell setup files. <br>
Risk: Synced Markdown files can contain private voice-note transcripts and AI summaries. <br>
Mitigation: Sync notes into a private directory and exclude that directory from public repositories or broad backups when appropriate. <br>
Risk: Large syncs can run into the Voicenotes API rate limit described by the artifact. <br>
Mitigation: Use incremental syncs with --since and avoid repeatedly fetching the full note history. <br>


## Reference(s): <br>
- [ClawHub Voicenotes release](https://clawhub.ai/shawnhansen/voicenotes) <br>
- [Voicenotes](https://voicenotes.com) <br>
- [Voicenotes token settings](https://voicenotes.com/app?obsidian=true#settings) <br>
- [Voicenotes Obsidian sync API base](https://api.voicenotes.com/api/integrations/obsidian-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; scripts return JSON and write Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOICENOTES_TOKEN; markdown sync also requires jq and may write local copies of transcripts and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
