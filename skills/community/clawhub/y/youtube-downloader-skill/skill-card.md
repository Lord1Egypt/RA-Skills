## Description: <br>
Download YouTube videos by URL in various resolutions using a pay-per-use API with credit-based authentication and no charge on failed downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jxyyjm](https://clawhub.ai/user/jxyyjm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to download YouTube videos or extract audio at requested resolutions through the skill.lordest.cn API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube URLs and an API key to the third-party skill.lordest.cn downloader service. <br>
Mitigation: Use a dedicated, revocable API key and avoid submitting private or sensitive video URLs. <br>
Risk: Successful downloads may consume account credits and produce hosted download links. <br>
Mitigation: Confirm the requested video and resolution before use, and share returned download links only with intended recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jxyyjm/youtube-downloader-skill) <br>
- [YouTube downloader service](https://skill.lordest.cn) <br>
- [API key management](https://skill.lordest.cn/?page=apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell Commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline JSON, bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted download links, video metadata, account status, or error responses from the third-party service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
