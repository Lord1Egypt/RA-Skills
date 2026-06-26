## Description: <br>
Aligns two or more video or audio recordings of the same event to a common timeline and produces lightweight `.sync.json` sidecars without modifying the original media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and production engineers use this skill to align multicamera and separate-audio recordings before downstream editing, especially when sources start at different times or cover only part of an event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes user-selected local media and writes `.sync.json` sidecars next to those files. <br>
Mitigation: Run it only on intended media directories and review generated sidecars before using them in downstream editing workflows. <br>
Risk: The workflow depends on local ffmpeg, ffprobe, Python, NumPy, and SciPy installations. <br>
Mitigation: Use trusted package sources and verify those local dependencies before running the scripts on important media. <br>
Risk: The documentation contains a stale note about `_synced.MOV` output that conflicts with the current sidecar-only behavior reported by the security evidence. <br>
Mitigation: Treat `.sync.json` sidecars as the authoritative output, check the working directory for unexpected media files, and update the documentation before relying on it operationally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jianshuo/wjs-syncing-multicam) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON sidecar schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The companion scripts write `.sync.json` sidecars next to the selected media files; original media files are intended to remain unchanged.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
