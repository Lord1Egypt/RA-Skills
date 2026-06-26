## Description: <br>
Content Catcher captures web pages and media into Markdown, PDF, JSON, structured extracts, summaries, translations, and downloadable video assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content operations users can use this skill to extract web content, convert pages to Markdown or PDF, analyze page text, capture structured data, and download supported video or M3U8 media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation, media-key handling, cookie/header rewriting, and data-forwarding behavior may expose sensitive page content, URLs, cookies, headers, or download metadata. <br>
Mitigation: Use the skill in an isolated workspace, avoid authenticated or sensitive pages unless necessary, do not provide cookies or session-bound URLs casually, and review any configured send-to-local destination before use. <br>
Risk: Captured URLs and download metadata may remain in local clip history or browser localStorage. <br>
Mitigation: Clear the .clips history and browser localStorage after use when captured URLs, media links, or download metadata are sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown, JSON, PDF, extracted media metadata, downloaded media files, and command-line guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local clip history, extracted content files, PDFs, media fragments, and downloaded video outputs depending on the command used.] <br>

## Skill Version(s): <br>
4.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
