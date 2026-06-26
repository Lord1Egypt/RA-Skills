## Description: <br>
Seedance Cog helps agents generate cinematic videos through CellCog and ByteDance's Seedance model, including multi-shot narratives, voice synthesis, lipsync, scoring, and editing from a single prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to ask an agent to generate marketing, explainer, cinematic, or spokesperson videos through CellCog and Seedance from a text prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded assets, and generated media may be handled by CellCog or Seedance. <br>
Mitigation: Use the skill only when that provider is approved for the task, and avoid submitting secrets, regulated data, or confidential material unless explicitly authorized. <br>
Risk: Synthetic voice, lipsync, and spokesperson outputs can create consent and disclosure risks. <br>
Mitigation: Use synthetic presenters, voices, and likenesses only with proper consent and clear disclosure. <br>
Risk: The skill requires a CELLCOG_API_KEY credential. <br>
Mitigation: Store the key in the environment, avoid pasting it into prompts or generated files, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [CellCog Homepage](https://cellcog.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/nitishgargiitd/seedance-cog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides CellCog API usage and setup; generated media is produced by the external CellCog/Seedance service.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
