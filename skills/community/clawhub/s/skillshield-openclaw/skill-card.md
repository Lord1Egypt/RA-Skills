## Description: <br>
Sandboxed command runner for AI agents that validates and isolates shell actions inside a Bubblewrap user namespace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[star8592](https://clawhub.ai/user/star8592) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route shell commands through a local safety layer that evaluates requests and executes approved commands in a Bubblewrap sandbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence rates the release as suspicious because it overstates its safeguards and leaves a local command-execution daemon running after use. <br>
Mitigation: Review before installing, use only in a controlled workspace, and stop the background daemon when finished. <br>
Risk: Commands are wrapped by Bubblewrap but can still change files in the current directory. <br>
Mitigation: Run only in an isolated project or disposable workspace and inspect proposed commands before execution. <br>
Risk: The scanner found this to be a Bubblewrap wrapper around arbitrary shell commands, not a complete approval, audit, or loop-prevention system. <br>
Mitigation: Treat the sandbox as one control among several, keep human review for sensitive commands, and clear the daemon cache after use when appropriate. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/star8592/skillshield-openclaw) <br>
- [Homepage](https://coinwin.info) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Command-line stdout, stderr, exit codes, and concise setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux with Bubblewrap, cargo, curl, and python3; runs commands through a local daemon and can write in the current workspace.] <br>

## Skill Version(s): <br>
2.1.8 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
