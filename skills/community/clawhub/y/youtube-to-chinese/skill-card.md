## Description: <br>
将提供的 YouTube 视频链接转录成完整中文稿，包含内容摘要和视频核心亮点，便于快速理解和复习。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WebGuHui](https://clawhub.ai/user/WebGuHui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn YouTube videos into Chinese transcripts, concise summaries, and key highlight notes for review or reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using browser:chrome can expose sensitive YouTube login session cookies to the download tool. <br>
Mitigation: Prefer public videos without cookies; when cookies are required, use a narrowly exported cookies.txt file and avoid broad browser-session access. <br>
Risk: Installing yt-dlp from an unverified source can introduce supply-chain risk. <br>
Mitigation: Install yt-dlp only through a trusted or verified method before running the download script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WebGuHui/youtube-to-chinese) <br>
- [Publisher profile](https://clawhub.ai/user/WebGuHui) <br>
- [yt-dlp release download](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp) <br>
- [Get cookies.txt LOCALLY Chrome extension](https://chrome.google.com/webstore/detail/get-cookiestxt-locally) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with Chinese transcript sections, summary bullets, highlight bullets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a complete Chinese transcript, a 3-5 sentence content summary, and 5-8 core highlights.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
