## Description: <br>
Generates minimalist geometric WeChat Mini Program TabBar icon PNGs for unselected and selected states, then updates app.json with the corresponding icon paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowstart](https://clawhub.ai/user/flowstart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building WeChat Mini Program projects use this skill to create consistent TabBar icons and wire those icons into the project's tabBar configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to write icon files and change app.json in a WeChat Mini Program project. <br>
Mitigation: Use it only in the intended project, keep version control or a backup, and review the generated images and app.json diff before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flowstart/wx-tabbar-icons) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python/Pillow code and JSON configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create 81x81 PNG files under images/ and update app.json when applied in a project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
