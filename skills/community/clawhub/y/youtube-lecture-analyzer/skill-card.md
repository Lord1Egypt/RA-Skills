## Description: <br>
Extracts YouTube lecture subtitles and generates structured analysis with key points, evidence, action items, and Chinese and English summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wallfacer-web](https://clawhub.ai/user/wallfacer-web) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, educators, writers, and learning-focused agents use this skill to fetch subtitles for a user-selected YouTube lecture and turn them into reviewable structure, summaries, key questions, concepts, and action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript requests are configured to use a local HTTP/HTTPS proxy at 127.0.0.1:26739. <br>
Mitigation: Run the skill only when you trust the local proxy service, or adjust the proxy configuration before use. <br>
Risk: Fetched transcript content is saved in a local analysis report. <br>
Mitigation: Run the skill in a directory where transcript reports are acceptable, and delete or secure generated reports when they contain sensitive material. <br>
Risk: The analysis depends on available subtitles and simple transcript-derived summarization. <br>
Mitigation: Review conclusions against the source video or transcript before using them for teaching, publication, or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wallfacer-web/youtube-lecture-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/wallfacer-web) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Command-line instructions and UTF-8 text report with structured lecture analysis and Chinese and English summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local lecture_analysis_<video_id>.txt report containing summaries and transcript-derived text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
