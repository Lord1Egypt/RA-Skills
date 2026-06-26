## Description: <br>
Creates shareable quote and reflection posters from book or film inputs using Mew image and design APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn book or film titles, quotes, takeaways, mood, and optional reference images into polished social check-in posters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a mew.design API key in the conversation. <br>
Mitigation: Use a revocable key, reuse only a previously validated key in the current conversation, and request a replacement only when the key is missing, invalid, expired, deactivated, or explicitly changed by the user. <br>
Risk: Selected quotes, reference image URLs, and explicitly approved uploaded images may be sent to external services for poster generation. <br>
Mitigation: Prefer public image URLs, explain when a local image needs external hosting, and obtain user consent before uploading any local or attached image to a third-party host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuminliu026/quote-checkin-poster) <br>
- [Mew image-process API endpoint](https://api.mew.design/open/api/image/process) <br>
- [Mew design-generate API endpoint](https://api.mew.design/open/api/design/generate) <br>
- [Mew account and API key setup](https://mew.design/login) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with image links and concise mood summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl examples for Mew API calls and guidance for style or mood retries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
