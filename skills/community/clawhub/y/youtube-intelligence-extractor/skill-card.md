## Description: <br>
Extracts structured intelligence from YouTube video transcripts for productivity, AI prompting, platform engineering, and creative workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erickgrau](https://clawhub.ai/user/erickgrau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and productivity-focused users use this skill to turn YouTube URLs, video IDs, or pasted transcripts into actionable reports with todos, frameworks, runnable prompts, and engineering or creative insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to automatically save markdown report files after presenting results. <br>
Mitigation: Use it only where persistent local report storage is acceptable, and review saved reports before sharing or retaining sensitive transcript-derived content. <br>
Risk: The skill instructs the agent to update its own SKILL.md after runs that reveal improvements. <br>
Mitigation: Prevent or review attempted edits to SKILL.md before accepting changes. <br>
Risk: Transcript fetching can involve third-party transcript sources or YouTube transcript tooling. <br>
Mitigation: Avoid private videos or sensitive transcripts unless third-party fetching and local report storage are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erickgrau/youtube-intelligence-extractor) <br>
- [Wave Tube transcript URL pattern](https://tube.wave.co/[video-slug]-[VIDEO_ID]) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with checklists, structured sections, and fenced code blocks for extracted prompts or commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a markdown report file after generating the chat response.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
