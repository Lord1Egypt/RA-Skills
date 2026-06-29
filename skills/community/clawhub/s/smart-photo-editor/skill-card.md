## Description: <br>
AI-powered photo editing and restoration skill - smart object removal, background removal, old photo restoration, and basic edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route photo-editing requests to Seedream, ImageMagick, OpenCV, and rembg for object removal, restoration, background removal, retouching, cropping, compression, and color adjustments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud AI editing can send selected photos to VolcEngine/Seedream. <br>
Mitigation: Avoid processing sensitive personal or business images with remote AI features unless that data sharing is acceptable. <br>
Risk: Edited outputs preserve EXIF metadata by default, which can retain camera or location information. <br>
Mitigation: Strip EXIF metadata before public sharing when privacy matters. <br>
Risk: The EXIF strip utility can overwrite the original image when no output path is provided. <br>
Mitigation: Provide an explicit output path when stripping metadata to preserve the source file. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/guoxh/smart-photo-editor) <br>
- [VolcEngine Ark Seedream setup documentation](https://www.volcengine.com/docs/82379/2375486) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code snippets, JSON examples, and generated image file outputs from invoked tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI editing requires network access to VolcEngine Ark/Seedream; local deterministic operations use ImageMagick, OpenCV, rembg, and EXIF utilities.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
