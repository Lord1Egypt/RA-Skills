## Description: <br>
Automatically fetch YouTube video subtitles and generate concise summaries for public videos with available captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[potatosolo](https://clawhub.ai/user/potatosolo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to extract key points, executive summaries, and optional detailed notes from public YouTube videos without watching the full video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends provided public YouTube video IDs through the YouTube transcript library to fetch captions. <br>
Mitigation: Use it only with videos appropriate for that dependency, and review or pin youtube-transcript-api in sensitive environments. <br>
Risk: Summaries depend on available captions and can be incomplete or misleading when captions are missing, auto-generated, or inaccurate. <br>
Mitigation: Review important summaries against the source video or transcript before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and formatted transcript text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports short, medium, or detailed summaries when captions are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
