## Description: <br>
Guides agents through configuring and using the SeedDance AI video generation API for text-to-video, image-to-video, and related video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AshwinRamachandran2002](https://clawhub.ai/user/AshwinRamachandran2002) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to integrate SeedDance video generation into Node.js workflows, including SDK installation, API key setup, configuration, text-to-video and image-to-video examples, batch handling, webhooks, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to install a third-party npm package. <br>
Mitigation: Verify that seeddance-sdk is the intended package and publisher before installing it. <br>
Risk: The workflow uses a SeedDance API key. <br>
Mitigation: Store SEEDDANCE_API_KEY in a secret manager or private environment file and avoid committing it. <br>
Risk: Prompts, images, and videos may be sent to a third-party AI video service. <br>
Mitigation: Avoid submitting sensitive media or prompts unless that use is approved for the service. <br>
Risk: Webhook examples send task callbacks to a user-controlled URL. <br>
Mitigation: Use only webhook URLs you control and can secure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AshwinRamachandran2002/seeddance-ai-video) <br>
- [SeedDance console](https://console.seeddance.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash, JSON, environment variable, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, API examples, webhook usage, error handling, and pricing notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
