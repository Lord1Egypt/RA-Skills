## Description: <br>
u2-downloader helps agents request YouTube video or audio downloads by URL through the disclosed u2foru.site API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XJouska](https://clawhub.ai/user/XJouska) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to ask an agent to download a YouTube video or audio-only extract by URL after supplying an API key for u2foru.site. Users should only use it for content they have rights to download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested YouTube URLs and an API key to the third-party u2foru.site service. <br>
Mitigation: Install only if you trust that service, avoid sensitive or private URLs, and rotate or revoke the API key if it is exposed. <br>
Risk: The skill can be used to download media from YouTube. <br>
Mitigation: Use it only for content you have the rights to download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XJouska/u2-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/XJouska) <br>
- [u2foru.site](https://u2foru.site) <br>
- [u2foru.site API keys](https://u2foru.site/?page=apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage guidance and download request examples; successful API responses may include a download URL, title, duration, file size, selected resolution, and processing time.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
