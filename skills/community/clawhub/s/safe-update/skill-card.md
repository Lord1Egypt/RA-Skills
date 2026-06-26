## Description: <br>
Update OpenClaw from source code. Supports custom project path and branch. Includes pulling latest branch, rebasing, building and installing, restarting service. Triggered when user asks to update OpenClaw, sync source, rebase branch, or rebuild. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HackSing](https://clawhub.ai/user/HackSing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to update an OpenClaw source checkout, preserve configuration backups, build and globally install the updated package, and restart the gateway service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change an OpenClaw source checkout, build and globally install code, copy configuration and auth-profile backups, and restart the OpenClaw gateway. <br>
Mitigation: Run it only against the intended checkout after reviewing the target directory, branch, local changes, and backup location. <br>
Risk: The security guidance states that dry-run is not fully non-mutating. <br>
Mitigation: Treat dry-run as a cautious preview and review the commands and target state before allowing any update. <br>
Risk: The documentation includes force-push guidance that can affect remote branch history. <br>
Mitigation: Avoid force-push workflows unless the user understands and accepts the remote branch impact. <br>


## Reference(s): <br>
- [ClawHub safe-update skill page](https://clawhub.ai/HackSing/safe-update) <br>
- [OpenClaw upstream repository](https://github.com/openclaw/openclaw.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local git, npm, and systemctl operations when invoked by an agent.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
