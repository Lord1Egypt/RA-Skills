## Description: <br>
Helps agents create reproducible terminal recordings with Charmbracelet VHS by authoring, validating, rendering, and debugging .tape files for GIF, MP4, or WebM output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to script deterministic terminal demos, validate VHS tape files, render terminal recordings, and debug failures without relying on ambient shell state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering a VHS tape executes the scripted terminal commands, which can modify files, run project commands, or contact external services. <br>
Mitigation: Read tapes before execution, use small deterministic fixtures, validate syntax first, and review the target commands before rendering. <br>
Risk: Terminal recordings and VHS publishing can expose secrets, private paths, account prompts, or other sensitive local context. <br>
Mitigation: Scan tapes and generated recordings for secrets or private data, and only publish a specific rendered file after explicit approval. <br>


## Reference(s): <br>
- [Charmbracelet VHS](https://github.com/charmbracelet/vhs) <br>
- [VHS installation documentation](https://github.com/charmbracelet/vhs#installation) <br>
- [ClawHub skill page](https://clawhub.ai/tmchow/skills/vhs-terminal-recorder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and VHS .tape snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify .tape files and propose VHS render commands; rendered media files are produced by local VHS execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
