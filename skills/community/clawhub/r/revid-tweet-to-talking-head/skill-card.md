## Description: <br>
Turns an X/Twitter or LinkedIn post from a URL or pasted thread into a short talking-head video with avatar, voiceover, and captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and social media teams use this skill to repurpose an X/Twitter or LinkedIn post into a short avatar-led talking-head video for short-form channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends post content or URLs, avatar inputs, and the Revid API key to Revid. <br>
Mitigation: Use it only when that data can be shared with Revid, avoid private or sensitive material, and protect the API key as a sensitive credential. <br>
Risk: URL-based scraping can fail or pull unwanted surrounding content from social platforms. <br>
Mitigation: Prefer pasted thread text when available, and use the URL workflow only with a tight extraction prompt. <br>
Risk: Avatar images or character identities may raise rights or consent concerns. <br>
Mitigation: Use avatar images and characters only when you have the appropriate rights and consent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/api00/revid-tweet-to-talking-head) <br>
- [Revid Render API Endpoint](https://www.revid.ai/api/public/v3/render) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON, HTTP, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY and user-provided post text or URL plus an avatar image URL or character ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
