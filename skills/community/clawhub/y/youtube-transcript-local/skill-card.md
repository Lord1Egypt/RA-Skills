## Description: <br>
Extracts YouTube subtitles locally with yt-dlp and helps agents return transcript text or summaries without relying on an external transcript API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miku233333](https://clawhub.ai/user/miku233333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to extract subtitles from user-provided YouTube videos, save transcript files locally, and produce concise summaries or transcript-based notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install yt-dlp at runtime if it is not already available, changing the active Python environment. <br>
Mitigation: Install yt-dlp yourself in an isolated environment before running the skill. <br>
Risk: The skill invokes yt-dlp, contacts YouTube with supplied URLs, and writes transcript or cache files locally. <br>
Mitigation: Run it only with URLs you intend to process, choose a controlled output directory, and review or remove saved transcript and cache files when finished. <br>
Risk: The release security summary says the skill overstates its safety and under-discloses runtime package installation. <br>
Mitigation: Review the behavior before installation and treat the release as requiring extra scrutiny despite its advertised local execution model. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/miku233333/youtube-transcript-local) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with shell commands; generated transcript files may be SRT, VTT, or Markdown summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke yt-dlp, contact YouTube for supplied URLs, and save transcript or cache files locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
