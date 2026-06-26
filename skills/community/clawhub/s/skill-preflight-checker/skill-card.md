## Description: <br>
Skill Preflight Checker guides agents through pre-installation safety checks for skills, including author reputation, suspicious scripts, permission needs, isolated testing, and install recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill before installing ClawHub, GitHub, or package-based skills to produce a structured safety report and install recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad package or file scans could expose sensitive local folders if run directly against a personal workspace. <br>
Mitigation: Confirm the exact target before scanning, avoid broad scans of sensitive directories, and run checks in an isolated workspace or container. <br>
Risk: Preflight recommendations can be incomplete or produce false positives when package reputation or metadata is unavailable. <br>
Mitigation: Review the generated report and manually verify unclear findings before installing or rejecting a skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skill-preflight-checker) <br>
- [Publisher profile](https://clawhub.ai/user/cp3d1455926-svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces risk levels and install recommendations such as safe, cautious, or reject.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
