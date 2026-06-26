## Description: <br>
Fetches a known URL and returns page content as markdown, plain text, raw HTML, or a downloaded image file using a local Node.js helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shikamaru-cc](https://clawhub.ai/user/shikamaru-cc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a URL is already known and the task is retrieval, inspection, summarization, conversion, or saving a page asset rather than web discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch private or internal URLs if the agent is asked to do so. <br>
Mitigation: Use it only for intended URLs and avoid private or internal targets unless that access is explicitly required. <br>
Risk: Image downloads write to the requested output path. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important files. <br>
Risk: Fetched page content may be incomplete, blocked, misleading, or too large to retrieve. <br>
Mitigation: Treat fetched content as untrusted input, quote or summarize only relevant excerpts, and report fetch failures plainly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shikamaru-cc/shikamaru-web-fetch) <br>
- [Publisher profile](https://clawhub.ai/user/shikamaru-cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files] <br>
**Output Format:** [XML-like <web_fetch> block containing title, URL, MIME metadata, and either content text or a saved image path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports markdown, text, HTML, and image download outputs; rejects responses larger than 5MB; timeout is capped at 120 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
