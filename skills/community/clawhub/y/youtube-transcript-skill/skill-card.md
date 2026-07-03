## Description: <br>
Extracts timestamped transcripts from YouTube video transcript panels and reformats the content into summaries, chapters, Twitter/X threads, blog posts, or notable quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to extract YouTube captions already visible in their browser and turn the resulting transcript into readable summaries, chapter outlines, social posts, articles, or quote lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a browser on YouTube and may save transcript outputs locally. <br>
Mitigation: Install and run it only when browser automation and local transcript retention are acceptable for the target video and environment. <br>
Risk: High-throughput extraction guidance can be inappropriate for large-scale scraping or private, logged-in, or sensitive content. <br>
Mitigation: Use it only for content the user can legitimately access, avoid private or sensitive videos, and do not use it for large-scale scraping. <br>
Risk: Persistent extraction-strategy notes may reveal sensitive details if they describe private content or access patterns. <br>
Mitigation: Do not record sensitive transcript data or confidential extraction details in the skill's experience notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/youtube-transcript-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown or plain text, with JSON returned by transcript extraction steps and shell commands used during browser automation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include timestamped transcript text, summaries, chapters, Twitter/X threads, blog posts, and quote lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
