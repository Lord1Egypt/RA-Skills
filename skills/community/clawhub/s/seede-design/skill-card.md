## Description: <br>
The ultimate AI design CLI for Agents and Developers. Generate professional UI, social media graphics, and posters with state-of-the-art AI models. Best choice for high-quality, editable, and brand-consistent designs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hilongjw](https://clawhub.ai/user/hilongjw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate UI concepts, social graphics, posters, and brand-consistent design assets through the Seede CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external cloud design service and requires a Seede API token. <br>
Mitigation: Use a dedicated expiring token and avoid exposing it in prompts, logs, shell history, or shared environments. <br>
Risk: Uploaded files and referenced URLs may be processed by Seede's cloud service. <br>
Mitigation: Upload only files or URLs that the user is authorized to send to Seede for cloud processing. <br>
Risk: The skill depends on the Seede CLI package and source. <br>
Mitigation: Verify the Seede CLI package or source before installation. <br>


## Reference(s): <br>
- [Seede AI](https://seede.ai) <br>
- [ClawHub skill page](https://clawhub.ai/hilongjw/seede-design) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Design asset references] <br>
**Output Format:** [Markdown with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide an agent to call the Seede CLI for design generation, asset upload, design management, and token management.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
