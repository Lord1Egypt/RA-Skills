## Description: <br>
Headless creative production studio for AI agents that generates images, edits photos, creates video and audio assets, and assembles polished output via Remotion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohnen](https://clawhub.ai/user/cohnen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and AI agents use this skill to automate creative media production from brief planning through image, video, voice, music, sound effects, and Remotion assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, briefs, and selected media inputs may be sent to configured AI providers and may consume API credits. <br>
Mitigation: Avoid secrets or confidential campaign details in prompts, configure only trusted provider keys, and use dry-run mode before full pipelines. <br>
Risk: Generated media and task logs may be written to local output directories. <br>
Mitigation: Review output directories and task logs when handling sensitive creative work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cohnen/shellbot-creative-studio) <br>
- [ShellBot homepage](https://getshell.ai) <br>
- [Command reference](references/command-reference.md) <br>
- [Provider matrix](references/provider-matrix.md) <br>
- [Creative guidelines](references/creative-guidelines.md) <br>
- [Workflow recipes](references/workflow-recipes.md) <br>
- [Remotion playbook](references/remotion-playbook.md) <br>
- [Remotion rules index](references/remotion-rules-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status output, Markdown guidance, shell command invocations, generated media files, and Remotion project code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands support dry-run previews and write media assets, task logs, storyboard JSON, and rendered video outputs to local project directories.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
