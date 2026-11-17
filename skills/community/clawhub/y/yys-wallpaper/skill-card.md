## Description:

Yys Wallpaper helps an agent run a Python downloader for Onmyoji artwork wallpapers from the NetEase YYS media page, selecting supported resolutions and saving images under the user's Pictures directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhf6623](https://clawhub.ai/user/lhf6623)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to download, organize, or re-download Onmyoji wallpaper images in a selected resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader fetches many images from the internet and writes files under the user's home directory.

Mitigation: Review the destination path before running the script and use the documented resolution values and delay options.

Risk: Using the re-download option may overwrite expected skip behavior and increase network and disk usage.

Mitigation: Avoid --no-skip unless the destination directory has been reviewed and re-downloading is intentional.

Risk: The authoritative security summary flags broader filesystem handling than the description implies.

Mitigation: Review the script before installation and confirm that files are saved under ~/Pictures/{resolution}/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lhf6623/skills/yys-wallpaper)
- [Publisher profile](https://clawhub.ai/user/lhf6623)
- [NetEase YYS media picture page](https://yys.163.com/media/picture.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown with inline shell commands and Python script execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces downloaded image files under ~/Pictures/{resolution}/ when the script is executed.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
