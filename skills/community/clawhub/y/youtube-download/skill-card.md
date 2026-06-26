## Description: <br>
Downloads YouTube videos to ~/Downloads when the user wants a local copy on their machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bestisblessed](https://clawhub.ai/user/bestisblessed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download a user-provided YouTube URL into the local ~/Downloads folder with yt-dlp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates video files in ~/Downloads, which can consume local storage. <br>
Mitigation: Review expected file size before downloading large videos and remove unwanted files after use. <br>
Risk: Downloaded content may be restricted by copyright or site policy. <br>
Mitigation: Download only content the user is permitted to save under applicable rights and platform rules. <br>
Risk: The skill depends on the local yt-dlp executable. <br>
Mitigation: Install yt-dlp from the declared package-manager path and keep it updated before running downloads. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Shell command output and downloaded MP4 file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves video files under ~/Downloads using yt-dlp best-available video and audio merge settings.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
