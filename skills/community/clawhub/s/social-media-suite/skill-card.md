## Description: <br>
Automate social media posting to Instagram and YouTube. Schedule and publish images, videos, and content automatically. Social media automation tool for content creators, marketers, and businesses. Free alternative to Buffer and Hootsuite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vitja1988](https://clawhub.ai/user/Vitja1988) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketing teams, business owners, and agencies use this skill to prepare command-line workflows for posting Instagram images and YouTube videos with captions, privacy settings, tags, and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact documents command flows but does not include the referenced run.sh, instagram_poster.sh, or youtube_uploader.sh implementation scripts. <br>
Mitigation: Treat the release as documentation until implementation files are supplied and reviewed before execution. <br>
Risk: The skill asks users to store powerful Instagram and YouTube credentials. <br>
Mitigation: Keep credential files outside shared or synced folders, restrict file permissions, exclude them from version control, and rotate tokens if exposed. <br>
Risk: Posting commands can publish public social media content. <br>
Mitigation: Review generated captions, media, tags, and privacy settings before posting or uploading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vitja1988/social-media-suite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents credential setup and posting commands; referenced implementation scripts are not included in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
