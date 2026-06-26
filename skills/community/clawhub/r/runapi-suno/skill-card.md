## Description: <br>
Generate and transform music with Suno through RunAPI, using the RunAPI CLI for one-off agent tasks and SDKs for application integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create, extend, transform, and inspect music or audio through RunAPI's Suno service. It helps agents choose CLI commands for one-off work and SDK packages for app, backend, worker, or library integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generated audio, and authentication are handled by RunAPI/Suno, a third-party service. <br>
Mitigation: Avoid submitting private, regulated, proprietary, or copyrighted material unless authorized and comfortable with the provider's data handling and terms. <br>
Risk: The skill can use sensitive RunAPI credentials through login state or RUNAPI_API_KEY. <br>
Mitigation: Store credentials securely, avoid placing keys in prompts or committed files, and rotate credentials if exposure is suspected. <br>
Risk: Music generation may involve provider billing, rate limits, and rights obligations. <br>
Mitigation: Review RunAPI/Suno pricing, rate limits, and usage terms before running production or high-volume requests. <br>


## Reference(s): <br>
- [RunAPI Suno model homepage](https://runapi.ai/models/suno) <br>
- [RunAPI Suno model overview, pricing, and rate limits](https://runapi.ai/models/suno.md) <br>
- [RunAPI Suno provider comparison](https://runapi.ai/providers/suno.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-suno) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, package names, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference the runapi CLI, RunAPI SDK packages, optional RUNAPI_API_KEY authentication, and request JSON files.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
