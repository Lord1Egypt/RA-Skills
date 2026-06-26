## Description: <br>
Convert SRT subtitle files into Remotion typing-animation videos with character-by-character text reveal and cinematic animated backgrounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x00000003](https://clawhub.ai/user/0x00000003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video creators use this skill to turn standard SRT subtitle files into local Remotion projects with timed typewriter captions and animated backgrounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and rendering the generated Remotion project may require npm network access and executes local project scripts. <br>
Mitigation: Review generated files first, then run npm install and render commands in a normal project directory or sandbox appropriate for the user's environment. <br>
Risk: The artifact templates may not include every Remotion entry or composition file needed for a runnable project. <br>
Mitigation: Confirm the generated project contains the required entry, composition, package, and TypeScript files before previewing or rendering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x00000003/srt-to-video) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/0x00000003) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with TypeScript/React project files and npm command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local Remotion project structure intended for preview and rendering after dependency installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
