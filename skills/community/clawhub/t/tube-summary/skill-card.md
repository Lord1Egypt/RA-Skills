## Description: <br>
Searches YouTube for videos on a topic, extracts English subtitles, and produces summaries with key topics, timestamps, and quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dillera](https://clawhub.ai/user/dillera) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and researchers use this skill to find YouTube videos on a topic and quickly understand selected videos from available subtitle text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts YouTube and depends on third-party tooling before it can search videos or fetch subtitles. <br>
Mitigation: Install only from a trusted source, verify required tools such as yt-dlp and Python packages, and run the workflow in a normal non-privileged environment. <br>
Risk: Subtitle files are created in the directory where the subtitle download command is run. <br>
Mitigation: Run subtitle extraction from a dedicated working folder and review generated files before sharing or reusing them. <br>
Risk: Summaries are based on available subtitles, which may be missing, auto-generated, incomplete, or inaccurate. <br>
Mitigation: Treat generated summaries, quotes, and timestamps as aids for review and check important claims against the original video. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dillera/tube-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted summaries and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include search-result lists, video URLs, key topics, concise summaries, timestamps, and key quotes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
