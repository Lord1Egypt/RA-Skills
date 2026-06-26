## Description: <br>
Processes videos by converting formats, compressing files, trimming clips, adding subtitles, and extracting covers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare video assets by converting common formats, reducing file size, clipping content, adding subtitles, and extracting cover images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local video processing may require enough temporary disk space for large input files. <br>
Mitigation: Confirm available storage before running long or large processing jobs and clean temporary files after use. <br>
Risk: The skill depends on local video-processing tools and includes an unexplained curl dependency. <br>
Mitigation: Confirm the package source is trusted and review expected dependency use before installing or processing private videos. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local video-processing dependencies such as ffmpeg and temporary disk storage.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
