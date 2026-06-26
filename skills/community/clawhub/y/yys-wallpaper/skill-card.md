## Description: <br>
Yys Wallpaper helps an agent run a Python downloader that fetches NetEase Onmyoji wallpaper images by resolution and saves them under the user's Pictures directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhf6623](https://clawhub.ai/user/lhf6623) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to download or organize Onmyoji wallpapers in supported desktop or mobile resolutions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader contacts NetEase wallpaper pages and image URLs over the network. <br>
Mitigation: Install and run the skill only when NetEase Onmyoji wallpaper downloads are intended. <br>
Risk: Wallpaper downloads can consume significant local storage, especially at 1920x1080 where the documentation estimates about 2.1GB. <br>
Mitigation: Choose the needed resolution, keep skip-existing behavior enabled by default, and confirm available disk space before large batches. <br>
Risk: Using --no-skip can re-download files that already exist. <br>
Mitigation: Use --no-skip only when intentionally refreshing or replacing local wallpaper files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhf6623/yys-wallpaper) <br>
- [NetEase Onmyoji wallpaper page](https://yys.163.com/media/picture.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The downloader writes wallpaper image files under ~/Pictures/{resolution}/ and prints console progress.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
