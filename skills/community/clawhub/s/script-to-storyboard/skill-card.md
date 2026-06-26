## Description: <br>
Converts film or video scripts into structured storyboard tables with shot numbers, camera framing and angles, visual content, characters, scenes, and sound notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eita19](https://clawhub.ai/user/Eita19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and production teams use this skill to turn script text into storyboard planning tables. It supports both manual conversion guidance and a local helper script that parses shot cues and writes a CSV storyboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper reads script content from the selected input file and writes a CSV file to the selected output path. <br>
Mitigation: Process only scripts suitable for the local agent workflow, and choose a non-critical output filename to avoid overwriting important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Eita19/script-to-storyboard) <br>
- [Publisher profile](https://clawhub.ai/user/Eita19) <br>
- [Example storyboard](references/示例分镜.md) <br>
- [Example script](references/示例剧本.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, console table text, and CSV storyboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper reads a user-selected input script file and writes a CSV file to the chosen output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
