## Description: <br>
Generate and edit video with Hailuo through RunAPI, routing one-off generation tasks to the RunAPI CLI and application or backend integrations to SDKs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate, edit, or transform video with Hailuo through the RunAPI CLI for one-off tasks, or to choose SDK packages when integrating RunAPI into an application or backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party RunAPI CLI and Homebrew tap. <br>
Mitigation: Confirm the RunAPI CLI and Homebrew tap are trusted before installation or execution. <br>
Risk: Video prompts, images, and request files may be sent to RunAPI/Hailuo. <br>
Mitigation: Review RunAPI and Hailuo pricing and data-handling terms before sending sensitive or proprietary inputs. <br>
Risk: Authentication may use a RunAPI API key. <br>
Mitigation: Prefer a scoped API key when possible and avoid embedding credentials in prompts, source files, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-hailuo) <br>
- [RunAPI Hailuo model overview](https://runapi.ai/models/hailuo) <br>
- [RunAPI Hailuo model documentation](https://runapi.ai/models/hailuo.md) <br>
- [RunAPI Minimax provider documentation](https://runapi.ai/providers/minimax.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use the runapi CLI for one-off video tasks and SDK package names for application integration.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
