## Description:

读取微信公众号文章的专用工具，支持OCR文字识别。自动规范化URL并提取文章内容，识别图片中的中英文文字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[2720480371](https://clawhub.ai/user/2720480371)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read WeChat public-account articles, normalize WeChat article URLs, extract article text, and run OCR over article images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests beyond its intended WeChat article-reading purpose.

Mitigation: Use it only in an environment where outbound requests are contained, and review URL handling before processing untrusted or attacker-provided URLs.

Risk: Image fetching and OCR can be abused to consume network, CPU, memory, or runtime resources.

Mitigation: Limit image count, download size, redirects, and OCR runtime before deployment.

Risk: Untrusted URLs or redirects could reach private or internal addresses.

Mitigation: Enforce HTTPS mp.weixin.qq.com article URLs, validate image CDN destinations, and block private or internal network addresses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2720480371/skills/wechat-look)
- [Node.js](https://nodejs.org/)
- [Python](https://python.org/)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON with extracted article fields and OCR text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns title, author, text content, image count, OCR text, normalized URL, and status when article extraction succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
