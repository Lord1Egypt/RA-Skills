## Description: <br>
Reverse image search: find where an image appears on the web, visually similar images, and what the image contains from an image URL or uploaded image file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[selvatuple](https://clawhub.ai/user/selvatuple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for an image's source, online matches, visually similar images, and related entities. It supports both direct image URLs and uploaded image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs or uploaded image files are sent to SearchThisImage for reverse image search processing. <br>
Mitigation: Avoid private, regulated, or confidential images unless the provider's privacy terms meet the user's needs. <br>
Risk: The skill requires an API key for SearchThisImage. <br>
Mitigation: Use a dedicated API key and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Uploaded image searches may require a temporary local image file. <br>
Mitigation: Delete temporary image files after the search completes. <br>


## Reference(s): <br>
- [SearchThisImage API](https://api.searchthisimage.com) <br>
- [SearchThisImage privacy policy](https://searchthisimage.com/privacy.html) <br>
- [ClawHub skill page](https://clawhub.ai/selvatuple/searchthisimage) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with links; API responses are JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SEARCHTHISIMAGE_API_KEY; lists up to 5 matching pages and 3 visually similar image URLs when available] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
