## Description: <br>
Spin up a one-time web UI for securely entering secret keys and env vars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awlevin](https://clawhub.ai/user/awlevin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create a temporary portal for collecting API keys or environment variables without placing secret values in chat history or terminal logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users enter secrets into an external CLI-launched temporary web UI. <br>
Mitigation: Verify the package and tunnel tooling before using production keys, keep the generated portal URL private, and use the portal only for intended recipients. <br>
Risk: Secrets are saved to a local env file path selected at launch. <br>
Mitigation: Choose the env-file path deliberately, confirm file permissions, and delete or rotate saved secrets when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awlevin/secret-portal) <br>
- [Publisher profile](https://clawhub.ai/user/awlevin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI usage guidance for launching a temporary secret-entry portal and selecting an env-file destination.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
