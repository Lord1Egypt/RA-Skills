## Description: <br>
Download videos from Xiaohongshu (小红书) pages when the user wants to save a video from a xiaohongshu.com URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HViktorTsoi](https://clawhub.ai/user/HViktorTsoi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to extract real Xiaohongshu CDN video URLs and save the videos locally with browser automation, curl, or the bundled Python downloader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill visits Xiaohongshu and CDN pages and saves downloaded video files locally. <br>
Mitigation: Use it only when that network access and local file saving are expected, and keep the destination directory under the user's control. <br>
Risk: Untrusted page text or prompts could suggest unsafe output_dir or --filename values. <br>
Mitigation: Do not accept path separators such as ../ in output_dir or --filename values supplied by untrusted content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HViktorTsoi/xhs-video-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown with inline JavaScript and bash code blocks; optional local MP4 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser automation or a Python script to fetch Xiaohongshu pages, extract CDN video URLs, and save videos under a user-controlled output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
