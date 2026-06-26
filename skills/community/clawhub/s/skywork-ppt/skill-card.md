## Description: <br>
Skywork PPT helps agents generate new PowerPoint decks, imitate existing PPTX styles, edit presentations with natural-language instructions, convert NotebookLM exports into editable PPTX files, and perform local PPTX operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxcun17](https://clawhub.ai/user/gxcun17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, transform, and manage PowerPoint presentations through Skywork remote workflows and local PPTX utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files and prompts used in generation, imitation, editing, and conversion workflows are sent to Skywork for remote processing. <br>
Mitigation: Use the skill only with files and prompts you are comfortable sending to Skywork, and avoid sensitive or confidential content unless you trust that service. <br>
Risk: The skill requires a Skywork API key. <br>
Mitigation: Use a dedicated API key where possible, store it through the configured secret mechanism or environment variable, and avoid printing or sharing it. <br>
Risk: Local delete and reorder operations can change presentation structure or overwrite outputs if paths are chosen carelessly. <br>
Mitigation: Specify an explicit output path or keep a backup before running local operations that delete, reorder, extract, or merge slides. <br>
Risk: The workflow installs and uses Python dependencies for PPTX manipulation. <br>
Mitigation: Run dependencies in a virtual environment when possible to limit effects on the wider Python environment. <br>


## Reference(s): <br>
- [Skywork PPT on ClawHub](https://clawhub.ai/gxcun17/skywork-ppt) <br>
- [Skywork API key setup guide](references/apikey-fetch.md) <br>
- [Skywork](https://skywork.ai) <br>
- [Skywork API key settings](https://skywork.ai/?openApiKeySetting=1) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PowerPoint files with Markdown status text, shell command examples, local file paths, and download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote workflows can return generated or converted PPTX files; local operations can inspect, delete, reorder, extract, or merge PPTX slides.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
