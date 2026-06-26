## Description: <br>
Helps agents copy local images from restricted QQBot download paths into an image-readable media directory, then analyze them with the image tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HAHH9527](https://clawhub.ai/user/HAHH9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to inspect user-supplied QQBot images that were saved under a local path the image tool cannot read directly. It guides the agent to copy a specific image into an allowed media directory before analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copying local images into the media directory can duplicate private or sensitive files. <br>
Mitigation: Use the workflow only for specific images the user supplied or explicitly wants analyzed, avoid broad paths or whole directories, and delete copied files from ~/.openclaw/media afterward when the images are private or sensitive. <br>
Risk: A copied file may overwrite an existing file with the same name in the media directory. <br>
Mitigation: Use a unique filename, such as one with a timestamp or random suffix, before copying the image. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HAHH9527/qqbot-image-helper) <br>
- [Publisher profile](https://clawhub.ai/user/HAHH9527) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline bash commands and image-tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file-copy commands for user-selected local images; copied files can contain private or sensitive image content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
