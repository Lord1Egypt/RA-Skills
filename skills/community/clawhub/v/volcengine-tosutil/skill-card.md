## Description: <br>
Generates, previews, validates, and optionally executes Volcengine TOS tosutil commands for bucket and object operations, batch transfers, metadata updates, connectivity checks, and common error diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to turn TOS storage tasks into reviewed tosutil command previews, structured execution results, and diagnostic next steps. It is intended for workflows such as configuration checks, listing buckets or objects, uploads and downloads, deletion planning, metadata changes, capacity checks, and troubleshooting permission or network failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Volcengine Tosutil on ClawHub](https://clawhub.ai/volc-sdk-team/skills/volcengine-tosutil) <br>
- [tosutil documentation survey](references/doc-survey.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [JSON results with redacted command previews, execution evidence, and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-by-default; real execution requires --run, and destructive operations require explicit confirmation such as --yes.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
