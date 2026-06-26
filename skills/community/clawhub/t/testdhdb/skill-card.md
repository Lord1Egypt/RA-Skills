## Description: <br>
Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinjianfenghzau-wq](https://clawhub.ai/user/qinjianfenghzau-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to install the AI Assistant Security plugin package, start a remote authorization flow, and update local OpenClaw plugin configuration after authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer depends on the ClawSentry service and an external OpenClaw plugin package. <br>
Mitigation: Install only in environments where the ClawSentry service and @omni-shield plugin package are trusted. <br>
Risk: Login tokens, device fingerprints, and credential-bearing responses may be stored under `.state`. <br>
Mitigation: Protect or remove `login_state.json` and `poll_login.log` after setup, especially on shared systems. <br>
Risk: The skill changes local OpenClaw plugin configuration and restarts the OpenClaw gateway. <br>
Mitigation: Run it in a controlled OpenClaw environment and review configuration changes before using it with sensitive workloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinjianfenghzau-wq/testdhdb) <br>
- [Artifact README](artifact/README.md) <br>
- [Volcengine website](https://www.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and login URL guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation steps and operational guidance for an OpenClaw environment.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
