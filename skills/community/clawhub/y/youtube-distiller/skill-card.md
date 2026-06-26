## Description: <br>
Automatically downloads subtitles from YouTube and Bilibili videos and generates structured knowledge articles in multiple summary styles using AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumo0221](https://clawhub.ai/user/sumo0221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn YouTube or Bilibili video content into concise notes, action lists, investment summaries, news briefs, or other structured knowledge articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An exposed MiniMax API key appears in the release evidence. <br>
Mitigation: Remove the key from the artifact, rotate it, and require users to provide credentials through an environment variable or secret store. <br>
Risk: Transcript-derived content is sent to MiniMax for summarization with limited disclosure. <br>
Mitigation: Clearly disclose external AI processing and avoid private or sensitive videos unless that processing is acceptable. <br>
Risk: Generated summaries may be persisted locally and synced to SumoNoteBook by default. <br>
Mitigation: Make syncing explicit or opt-in, document local storage paths, and use the no-sync option when local persistence is not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sumo0221/youtube-distiller) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Development log](artifact/youtube-knowledge-dev.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [UTF-8 plain text or Markdown knowledge articles, with command-line invocation guidance when used interactively.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multiple summary styles and can persist generated summaries locally or sync them to SumoNoteBook unless syncing is disabled.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
