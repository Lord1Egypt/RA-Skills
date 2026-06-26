## Description: <br>
Download videos in MP4 format using yt-dlp with FaaS (Firecracker/Container) isolation. Start downloads, check status, and kill processes. Videos are automatically converted to MP4 format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LAsurvivor](https://clawhub.ai/user/LAsurvivor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to start, monitor, and stop long-running yt-dlp video downloads on local, remote, or headless systems while saving results as MP4 files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run long-lived local yt-dlp processes without proven container isolation. <br>
Mitigation: Install and use it only when local background downloads are acceptable, and monitor or stop sessions with the provided status and kill commands. <br>
Risk: Temporary session, PID, and log files are stored under /tmp and may expose download metadata on shared machines. <br>
Mitigation: Use trusted URLs, avoid private or tokenized video links on shared systems, and pass only session IDs produced by this skill. <br>
Risk: Force-killing downloads can leave partial output files. <br>
Mitigation: Prefer graceful termination and check the output directory for incomplete files after stopping a download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LAsurvivor/video-download-faas) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and generated local session, log, PID, and MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts long-running local background yt-dlp processes and reports session IDs for later status checks or termination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
