## Description: <br>
Analyzes TikTok, YouTube, Instagram, Twitter/X, and other supported video URLs by downloading audio, transcribing it locally, and answering questions about the content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[holl4ndtv](https://clawhub.ai/user/holl4ndtv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users use this skill to analyze video URLs, generate local transcripts, summarize content, answer questions, and search previously cached transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts are written locally by default even though the user-facing flow presents saving as optional. <br>
Mitigation: Review before installing; prefer an update that makes transcript retention truly opt-in and clearly discloses cache behavior. <br>
Risk: Saved transcript handling uses local filenames and passes raw transcript JSON through command arguments. <br>
Mitigation: Sanitize saved filenames, avoid passing raw transcript JSON through shell arguments, and restrict transcript directory permissions. <br>
Risk: The skill downloads media audio, installs or uses local transcription dependencies, and may download a transcription model on first run. <br>
Mitigation: Run only in environments where those network downloads and local storage behaviors are acceptable, and verify dependencies before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/holl4ndtv/tiktok-video-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/holl4ndtv) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and answers, with local helper scripts returning JSON to the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads audio with yt-dlp, transcribes locally, caches transcript JSON under the skill directory, and may reuse cached transcripts for follow-up questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
