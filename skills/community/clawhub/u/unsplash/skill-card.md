## Description: <br>
Search, browse, and download high-quality free photos from Unsplash with filtering, random selection, and detailed photo metadata access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brokenwatch24](https://clawhub.ai/user/Brokenwatch24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to work with the Unsplash API for photo search, random image selection, photo metadata lookup, image URL handling, and required download tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Unsplash API access key and can consume the user's Unsplash app quota. <br>
Mitigation: Use a dedicated Unsplash key, store it privately, monitor rate-limit headers, and avoid sharing the key in prompts, logs, or public files. <br>
Risk: Download-tracking calls affect Unsplash download metrics and should only be made for real downloads. <br>
Mitigation: Call the download endpoint only when the user actually intends to download an image, as the skill guidance describes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Brokenwatch24/unsplash) <br>
- [Unsplash Developers](https://unsplash.com/developers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential setup guidance, endpoint examples, request parameters, response structures, and usage cautions for rate limits and download tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
