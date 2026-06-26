## Description: <br>
Smart image loader that handles both URLs and local files, automatically downloads URLs to temporary locations, and displays images using the read tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tingwei1123](https://clawhub.ai/user/tingwei1123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to display images from trusted web URLs or local workspace paths. It helps an agent download URL images to a temporary file or resolve local image paths before using an image-reading tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary image URLs for display. <br>
Mitigation: Use trusted image URLs and avoid unusual filenames or query strings. <br>
Risk: The cleanup guidance could mishandle crafted filenames if raw shell removal is used. <br>
Mitigation: Clean up temporary files with Python file removal or safe argument passing instead of raw shell rm. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tingwei1123/smart-image-loader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text status fields with a local file path for the image-reading tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary image files for URL inputs; URL downloads require cleanup after display.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
