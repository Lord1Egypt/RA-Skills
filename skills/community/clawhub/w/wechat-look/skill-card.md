## Description: <br>
Reads WeChat public-account articles, normalizes article URLs, extracts page text, and uses OCR to recognize Chinese and English text in article images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2720480371](https://clawhub.ai/user/2720480371) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch WeChat article content and return extracted text plus OCR text from article images for downstream reading, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports captcha-bypass wording in the skill documentation. <br>
Mitigation: Remove bypass-oriented wording and document only normal URL handling and permitted access patterns. <br>
Risk: The security review reports that the skill can fetch unvalidated remote URLs and download referenced images. <br>
Mitigation: Restrict downloads to expected public WeChat and CDN image hosts, and enforce image count, size, and timeout limits. <br>
Risk: The skill fetches WeChat pages, downloads article images, and runs local Node OCR scripts. <br>
Mitigation: Review before installing, keep dependencies current, and run the skill in an environment where external network access and local process execution are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2720480371/wechat-look) <br>
- [Node.js](https://nodejs.org/) <br>
- [Python](https://python.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Structured JSON-like article extraction with title, author, text content, image count, OCR text, normalized URL, and status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OCR confidence, processing time, and per-image recognized text when the Node OCR path is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
