## Description: <br>
A web video downloader skill that helps an agent detect direct MP4, M3U8/HLS, segmented MP4, and blob-backed video sources from webpages and save them as complete MP4 files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieliuzhu888](https://clawhub.ai/user/xieliuzhu888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technically capable users use this skill to inspect webpages for video media sources, capture browser network requests when needed, and run the appropriate download or merge workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures browser request headers and signed media URLs during CDP network capture. <br>
Mitigation: Run capture in an isolated browser profile logged into only the minimum required sites, avoid unrelated tabs, and delete captured URL files after use. <br>
Risk: The shell scripts may download and execute a static ffmpeg binary when ffmpeg is not already installed. <br>
Mitigation: Prefer installing ffmpeg from a trusted package manager before using the skill, or review the download step before allowing it to run. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash commands and local JSON or MP4 file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write captured URL JSON to /tmp and downloaded or merged MP4 files to user-specified output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
