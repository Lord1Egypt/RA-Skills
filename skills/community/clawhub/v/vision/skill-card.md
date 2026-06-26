## Description: <br>
Resize, crop, convert, and optimize images using ImageMagick for image processing, format conversion, compression, and watermarking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to process local image files by resizing, cropping, converting formats, optimizing file size, inspecting metadata, and adding text watermarks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images can overwrite output paths selected by the user. <br>
Mitigation: Choose explicit output paths, review destinations before running commands, and keep backups of source images. <br>
Risk: Image metadata output can expose private EXIF details from personal photos. <br>
Mitigation: Treat metadata output as sensitive and avoid sharing EXIF details unless they have been reviewed or removed. <br>


## Reference(s): <br>
- [Vision on ClawHub](https://clawhub.ai/xueyetianya/vision) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, JSON] <br>
**Output Format:** [Image files plus plain text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ImageMagick tools and operates on user-selected input and output paths.] <br>

## Skill Version(s): <br>
3.5.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
