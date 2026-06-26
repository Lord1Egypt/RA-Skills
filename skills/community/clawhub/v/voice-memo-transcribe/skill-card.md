## Description: <br>
Transcribe Apple Voice Memos recordings to text, organize content, and save to Apple Notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[my12121-beep](https://clawhub.ai/user/my12121-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill on macOS to list iCloud-synced Apple Voice Memos, extract or generate transcripts, organize the content, and save reviewed notes to Apple Notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private voice recordings and transcript content. <br>
Mitigation: Review selected recordings and generated notes before saving or syncing them to Apple Notes/iCloud. <br>
Risk: The workflow may require Full Disk Access to read the local Voice Memos database and recordings. <br>
Mitigation: Install only when comfortable granting terminal access, and limit execution to the intended macOS account and recordings. <br>
Risk: Temporary note content may remain on disk at /tmp/note_content.txt. <br>
Mitigation: Delete /tmp/note_content.txt after saving or abandoning the note. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/my12121-beep/voice-memo-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, transcript text, structured note content, and optional JSON listings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create transcript files and temporary note content for review before saving to Apple Notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
