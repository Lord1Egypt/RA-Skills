## Description: <br>
Coordinates an end-to-end lofi ambience YouTube production workflow covering topic selection, AI image generation, Envato audio download, FFmpeg assembly, SEO packaging, upload scheduling, and Shorts slicing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylin19860916](https://clawhub.ai/user/kylin19860916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and channel operators use this skill to manage a full YouTube ambience-video release, from creative planning and asset generation through audio sourcing, video assembly, metadata preparation, publishing, and derivative Shorts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can give an agent broad access to local credentials, browser sessions, downloads, upload queues, and YouTube publishing actions. <br>
Mitigation: Use dedicated least-privilege credentials and require explicit confirmation before credential use, browser automation, downloads, upload-queue changes, scheduling, or publishing. <br>
Risk: Browser and CDP automation for Envato downloads may perform account actions or download files through an active browser session. <br>
Mitigation: Inspect referenced shared scripts before use, restrict downloads to the intended project directory, and confirm each download set before processing it. <br>
Risk: Automated upload scheduling can publish incorrect files, thumbnails, titles, descriptions, tags, or times if the queue is wrong. <br>
Mitigation: Review the generated publishing package and upload queue before running or allowing the YouTube upload step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylin19860916/withme-youtube) <br>
- [Content Matrix](references/content-matrix.md) <br>
- [With me. Style Guide](references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes human confirmation checkpoints for topic approval, FFmpeg review, and final publishing assets.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
