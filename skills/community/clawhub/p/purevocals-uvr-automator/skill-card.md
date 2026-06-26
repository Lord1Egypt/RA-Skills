## Description: <br>
PureVocals UVR Automator helps an agent run local audio separation workflows that extract vocals from individual audio files or batches of files while preserving folder structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and audio creators use this skill to prepare vocal-only tracks, acapella material, karaoke assets, and cleaned audio from supported audio files or directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that the skill downloads large third-party ML/audio packages, modifies Python packaging tools, creates persistent local environments and caches, and auto-installs ffmpeg. <br>
Mitigation: Run it in an isolated OpenClaw environment, container, or disposable account and review dependency sources before processing sensitive folders. <br>
Risk: Automatic model, package, and ffmpeg downloads can introduce network, disk usage, and supply-chain exposure during first run. <br>
Mitigation: Pre-stage reviewed dependencies and model files where possible, restrict network access when not needed, and monitor cache and output directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/purevocals-uvr-automator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wangminrui2022) <br>
- [UVR public model releases](https://github.com/TRvlvr/model_repo/releases/tag/all_public_uvr_models) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Shell commands and generated WAV audio files with brief status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local virtual environments, dependency caches, model caches, logs, and output folders.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
