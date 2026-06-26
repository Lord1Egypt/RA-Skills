## Description: <br>
Generate and edit video with InfiniteTalk through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to run InfiniteTalk video generation or editing jobs through the RunAPI CLI, and to identify SDK packages when integrating RunAPI into an application or backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunAPI credentials or saved CLI login state could be exposed if agents echo secrets, write them into shared files, or run in an untrusted environment. <br>
Mitigation: Treat RUNAPI_API_KEY and CLI login state as sensitive credentials; avoid printing secrets, scope access to trusted workspaces, and rotate credentials if exposure is suspected. <br>
Risk: Video generation inputs are sent to RunAPI and may incur usage costs or be subject to RunAPI rate limits and data handling terms. <br>
Mitigation: Review RunAPI pricing, rate limits, and data handling before running jobs, especially for large media inputs or automated workflows. <br>
Risk: Generated or edited video may not match the user's intent or may require review before use in downstream materials. <br>
Mitigation: Inspect generated outputs before publication or handoff, and rerun or revise request JSON when the result is unsuitable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-infinitetalk) <br>
- [RunAPI InfiniteTalk model overview](https://runapi.ai/models/infinitetalk) <br>
- [RunAPI InfiniteTalk model documentation](https://runapi.ai/models/infinitetalk.md) <br>
- [RunAPI Meigen AI provider comparison](https://runapi.ai/providers/meigen-ai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference RunAPI CLI authentication, request JSON files, asynchronous task IDs, and SDK package choices.] <br>

## Skill Version(s): <br>
0.2.4 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
