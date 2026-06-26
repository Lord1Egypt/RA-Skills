## Description: <br>
技术方案书全自动写作 - 多智能体协作、断点续作、完全自动化 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deardavidzheng](https://clawhub.ai/user/deardavidzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and proposal-writing teams use this skill to generate large Chinese technical proposal books with chapter planning, multi-agent chapter assignment, progress tracking, and continuation across context limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended continuation can keep reading and changing project files without fresh approval. <br>
Mitigation: Enable cron or HEARTBEAT continuation only for projects that should continue automatically, and keep those projects in a dedicated workspace. <br>
Risk: Automatic proposal generation may continue when the operator intended a project to pause. <br>
Mitigation: Set autoContinue to false for paused or review-gated projects and inspect progress.json before re-enabling continuation. <br>
Risk: Reference materials or copied agent directories may contain sensitive information. <br>
Mitigation: Review scripts, reference inputs, and agent directories before installation or migration, and avoid copying materials that contain secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deardavidzheng/tech-proposal-autopilot) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Quick guide](artifact/README.md) <br>
- [Detailed guide](artifact/GUIDE.md) <br>
- [Migration guide](artifact/MIGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown proposal files, JSON progress files, JavaScript helper scripts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project directories with outline, progress, continuation, chapter, final document, and log files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
