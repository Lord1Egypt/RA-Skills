## Description: <br>
Manages QQ Zone photo albums through QR login, album listing, photo browsing, upload, download, full-album backup, and album creation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wscats](https://clawhub.ai/user/Wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to back up, organize, browse, upload, download, and create QQ Zone photo albums through a local command-line workflow that uses QQ session cookies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses QQ session cookies with broad access to the user's QQ Zone photos. <br>
Mitigation: Keep cookies.json private, store it outside synced or shared folders, and delete or rotate it if exposure is suspected. <br>
Risk: Upload, create-album, and bulk download actions can modify or copy account photos at scale. <br>
Mitigation: Verify album IDs, output paths, upload files, and album-creation details before running commands that change or copy photos. <br>
Risk: The skill uses QQ Zone interfaces that may change without notice. <br>
Mitigation: Confirm login, listing, upload, and download behavior on a small album before relying on a bulk workflow. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/Wscats/qq-zone-photo) <br>
- [Publisher profile](https://clawhub.ai/user/Wscats) <br>
- [QQ Zone](https://user.qzone.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or read a local cookies.json file and may download photo files to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
