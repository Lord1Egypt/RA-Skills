## Description: <br>
Extracts YouTube video transcripts and subtitles through the YouMind API, batch-processing up to five videos and saving timestamped markdown transcripts to a YouMind board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DophinL](https://clawhub.ai/user/DophinL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve YouTube subtitles or transcripts, save the source video to YouMind, and receive transcript files suitable for review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad YouMind shell access. <br>
Mitigation: Review commands before execution and limit use to the documented install, board lookup, createMaterialByUrl, getMaterial, and transcript-file workflow. <br>
Risk: Video data may be sent to and saved in the user's YouMind account. <br>
Mitigation: Use the skill only for explicit transcript requests and avoid private or sensitive videos unless that storage is acceptable. <br>
Risk: The workflow requires an API key. <br>
Mitigation: Keep YouMind API keys in environment variables and do not paste them into chat. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/DophinL/youmind-youtube-transcript) <br>
- [Setup](references/setup.md) <br>
- [Environment configuration](references/environment.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Long-running tasks](references/long-running-tasks.md) <br>
- [YouMind API keys](https://youmind.com/settings/api-keys?utm_source=youmind-youtube-transcript) <br>
- [YouMind skills gallery](https://youmind.com/skills?utm_source=youmind-youtube-transcript) <br>
- [YouMind issue tracker](https://github.com/YouMindInc/youmind/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown transcript files with brief status messages, links, and optional summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes up to five YouTube URLs per batch and writes one transcript file per completed video.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
