## Description: <br>
Generates structured summaries and transcript-grounded Q&A for YouTube videos, with English and Hindi responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gangadharpadshetty](https://clawhub.ai/user/Gangadharpadshetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to process YouTube links, create concise summaries, and answer follow-up questions using transcript chunks returned by a trusted local backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a localhost backend that retrieves transcripts, creates embeddings, and stores video-derived data. <br>
Mitigation: Install and use it only when the localhost backend is trusted, and confirm its storage, retention, and deletion behavior before processing sensitive, private, or copyrighted videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gangadharpadshetty/youtube-summerizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with structured summaries, timestamps, takeaways, and transcript-grounded answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Hindi responses; answers should remain grounded in retrieved transcript chunks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
