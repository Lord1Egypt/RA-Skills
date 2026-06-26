## Description: <br>
Fetch YouTube video transcripts, metadata, and channel info with AI-powered summarization, key takeaway extraction, and multi-video analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch YouTube transcripts, metadata, channel listings, and search results, then optionally summarize, extract takeaways, compare videos, or ask questions using EvoLink AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted user or video text may be handled unsafely and run local Python code. <br>
Mitigation: Use only in controlled environments and avoid untrusted links or videos until text is passed as data rather than executable Python source. <br>
Risk: AI features transmit video transcript text and metadata to api.evolink.ai. <br>
Mitigation: Use AI commands only after accepting EvoLink data transmission; omit EVOLINK_API_KEY and use core commands when third-party transmission is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/youtube-assistant) <br>
- [EvoLink API Documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=youtube) <br>
- [YouTube Assistant GitHub Repository](https://github.com/EvoLinkAI/youtube-skill-for-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with optional shell commands and JSON-backed API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, yt-dlp, and curl; AI features require EVOLINK_API_KEY and send transcript text and metadata to api.evolink.ai.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
