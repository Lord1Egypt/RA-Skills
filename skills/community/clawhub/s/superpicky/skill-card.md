## Description: <br>
SuperPicky CLI wraps the SuperPicky bird-photo workflow with predictable install and run scripts for photo culling, bird identification, and eBird region-code lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoshino-s](https://clawhub.ai/user/yoshino-s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and invoke a local SuperPicky command-line workflow for bird-photo culling, image identification, species organization, and region-code lookup. It is intended for local photo-processing automation where the operator can review file changes before running destructive or metadata-writing commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation downloads mutable upstream SuperPicky code during setup. <br>
Mitigation: Install only from a trusted upstream source and review or pin the upstream commit before running the workflow. <br>
Risk: The --py helper can execute arbitrary Python scripts inside the skill virtual environment. <br>
Mitigation: Use --py only with known trusted helper scripts and avoid passing unreviewed paths from user input. <br>
Risk: Photo-processing commands can move files, reset folders, or write image metadata. <br>
Mitigation: Run commands on backed-up folders first, preview non-destructive modes where available, and use destructive flags such as -y, reset, restar, organize, or --write-exif only after confirming the target directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoshino-s/superpicky) <br>
- [SuperPicky upstream project](https://github.com/jamesphotography/SuperPicky) <br>
- [Reference index](reference/README-INDEX.md) <br>
- [Source metadata](reference/SOURCE.md) <br>
- [Captured CLI help](reference/cli-help-captured.txt) <br>
- [Manifest behavior notes](reference/manifest机制说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths, eBird country or region codes, SuperPicky command flags, and safety checks for photo-processing operations.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
