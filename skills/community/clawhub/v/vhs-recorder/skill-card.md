## Description: <br>
Create professional terminal recordings with VHS tape files - guides through syntax, timing, settings, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical writers, and CLI maintainers use this skill to draft VHS tape files and guidance for terminal demos, README animations, documentation videos, and social media recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or copied VHS tape examples can run destructive shell commands. <br>
Mitigation: Review every .tape file before running it, use a disposable workspace, and replace broad deletion examples with narrowly scoped demo resources. <br>
Risk: Examples include broad Docker cleanup commands that can affect unrelated containers. <br>
Mitigation: Use container names, labels, or project-specific IDs instead of commands that stop all running containers. <br>
Risk: Production database deletion examples could be copied into real environments. <br>
Mitigation: Keep destructive examples as non-executable teaching material and substitute safe test fixtures before recording. <br>


## Reference(s): <br>
- [VHS Tape File Syntax Reference](artifact/references/vhs-syntax.md) <br>
- [VHS Timing Control Reference](artifact/references/timing-control.md) <br>
- [VHS Settings Reference](artifact/references/settings.md) <br>
- [VHS Recording Examples](artifact/references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/killerapp/vhs-recorder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with VHS tape snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated .tape content, timing recommendations, VHS settings, and review guidance before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
