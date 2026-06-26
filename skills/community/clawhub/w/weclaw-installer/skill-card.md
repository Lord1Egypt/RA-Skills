## Description: <br>
Automate installing and configuring the WeClaw WeChat bot environment on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popilopi168](https://clawhub.ai/user/popilopi168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to bootstrap the WeClaw project locally on macOS, install Python dependencies with uv, configure the required API key, and resolve common macOS Accessibility setup blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup wrapper can run an unbundled local Python module while handling an API key. <br>
Mitigation: Inspect or obtain the exact setup_package.py that will run, preferably from a known source or pinned commit, before installing. <br>
Risk: The setup flow may handle secrets and can accept an API key on the command line. <br>
Mitigation: Use a least-privileged API key and avoid passing secrets on the command line when possible. <br>
Risk: The setup may require macOS Accessibility permissions. <br>
Mitigation: Enable Accessibility only for the trusted terminal or app intended to run the automation. <br>
Risk: The artifact includes ClawHub publish commands that are not needed for normal installation. <br>
Mitigation: Ignore the publish commands unless intentionally publishing this skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/popilopi168/weclaw-installer) <br>
- [WeClaw source repository](https://github.com/Popilopi168/weclaw-package-upload-test) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets macOS and expects git, uv, and python3 to be available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
