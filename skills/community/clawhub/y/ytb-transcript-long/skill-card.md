## Description: <br>
YouTube long video (>1 hour) full verbatim transcription and translation workflow for extracting subtitles, translating English transcripts to Chinese, handling long videos that exceed session limits, and generating formatted documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingliu1617-art](https://clawhub.ai/user/qingliu1617-art) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and content teams use this skill to obtain long YouTube transcripts, translate English transcript content into Chinese, and deliver the result as a Markdown file or document link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a published concrete API bearer token. <br>
Mitigation: Do not use the embedded bearer token; replace it with a protected DownSub credential before use. <br>
Risk: The workflow sends video URLs and transcript content to external services. <br>
Mitigation: Confirm with the user before sending private or unlisted video URLs to DownSub or uploading transcripts to zhiyan or another document service. <br>
Risk: The workflow may spawn long-running sub-agents for large transcripts. <br>
Mitigation: Confirm budget, runtime, and task boundaries before spawning long-running sub-agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingliu1617-art/ytb-transcript-long) <br>
- [DownSub API endpoint](https://api.downsub.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcript, translated Markdown document, or document link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process long transcripts in chunks and may use an external document service when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
