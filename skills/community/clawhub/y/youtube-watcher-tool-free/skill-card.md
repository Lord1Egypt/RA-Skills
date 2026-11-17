## Description: <br>
Extracts subtitles from a single YouTube video with yt-dlp and helps an agent summarize, search, answer questions about, or export the transcript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal learners, researchers, content creators, and language learners use this skill to retrieve subtitles from one YouTube video and turn the transcript into summaries, search results, Q&A answers, or exported text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may run yt-dlp commands, access YouTube, and write transcript files locally. <br>
Mitigation: Review commands before execution, install yt-dlp from a trusted source, and restrict use to intended YouTube subtitle extraction tasks. <br>
Risk: Private-video cookies, callback_url values, or exported transcripts can expose sensitive transcript data. <br>
Mitigation: Avoid cookies and callback URLs unless the endpoint is trusted, and keep transcript exports local or delete them after use. <br>
Risk: YouTube automatic subtitles may be incomplete or inaccurate. <br>
Mitigation: Prefer human CC subtitles when available and review summaries or Q&A answers against transcript text before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/youtube-watcher-tool-free) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transcript text for local export; output quality depends on subtitle availability and accuracy.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
