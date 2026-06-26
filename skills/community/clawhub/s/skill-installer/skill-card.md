## Description: <br>
Install, search, update, and manage skills from ClawHub, the public OpenClaw skill registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sreejith77](https://clawhub.ai/user/sreejith77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find, install, update, and inspect ClawHub skills from an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating skills can introduce persistent third-party behavior into future OpenClaw sessions. <br>
Mitigation: Review third-party skills before enabling them and restart the session only after confirming the installed skill is expected. <br>
Risk: The skill depends on the global npm `clawhub` CLI and the ClawHub registry supply chain. <br>
Mitigation: Install the CLI only after user confirmation and only if the user trusts ClawHub and the npm package. <br>
Risk: Using `clawhub update --all` may change multiple installed skills at once. <br>
Mitigation: Prefer targeted updates when reviewing changes matters, and inspect installed skills after broad updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sreejith77/skill-installer) <br>
- [ClawHub registry](https://clawhub.ai) <br>
- [Publisher profile](https://clawhub.ai/user/sreejith77) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install or update persistent OpenClaw skills.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
