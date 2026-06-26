## Description: <br>
Generate and edit images with Ideogram V3 through RunAPI, using the RunAPI CLI for one-off tasks and RunAPI SDKs for application integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate, edit, or remix images with Ideogram V3 through RunAPI. It helps route one-off creative requests to CLI commands and integration work to the appropriate SDK packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded images are sent to RunAPI/Ideogram when the skill is used for generation or editing. <br>
Mitigation: Review RunAPI pricing and data-handling terms before use, and avoid sensitive images or private creative material unless that use is approved. <br>
Risk: The CLI can authenticate with RUNAPI_API_KEY or saved RunAPI credentials. <br>
Mitigation: Store API keys in approved secret storage, avoid committing credentials, and prefer runapi login or scoped environment configuration where appropriate. <br>


## Reference(s): <br>
- [RunAPI Ideogram V3 homepage](https://runapi.ai/models/ideogram-v3) <br>
- [Ideogram V3 model overview, pricing, and rate limits](https://runapi.ai/models/ideogram-v3.md) <br>
- [Ideogram provider comparison](https://runapi.ai/providers/ideogram.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Ideogram V3 text-to-image action](https://runapi.ai/models/ideogram-v3/text-to-image.md) <br>
- [Ideogram V3 edit action](https://runapi.ai/models/ideogram-v3/edit.md) <br>
- [Ideogram V3 remix action](https://runapi.ai/models/ideogram-v3/remix.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell command examples and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runapi CLI for the CLI path; authentication can use runapi login, saved CLI configuration, or RUNAPI_API_KEY.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
