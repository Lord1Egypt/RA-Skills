## Description: <br>
Generate Marp teaching slides from source content for teachers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hh23333](https://clawhub.ai/user/hh23333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, course authors, and agents use this skill to turn one or more existing Markdown source files into a unified Marp slide deck. It plans the deck structure, applies the AM Blue Course theme and required slide conventions, preserves source-bounded content, and copies referenced images into the output folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent reads user-provided Markdown files and referenced images and writes a generated slide deck. <br>
Mitigation: Use the skill only with source files and images the agent is allowed to read, and review the generated deck before sharing it. <br>
Risk: Theme styling includes remote font and icon imports that may contact external services during rendering. <br>
Mitigation: For sensitive or offline use, vendor those assets locally or remove the remote imports before rendering. <br>


## Reference(s): <br>
- [Marp Slide Format Reference](artifact/references/marp-guide.md) <br>
- [Slide Generation Rules](artifact/references/rules.md) <br>
- [Awesome Marp](https://github.com/favourhong/Awesome-Marp) <br>
- [Marp](https://marp.app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown slide deck with Marp YAML, theme directives, layout classes, and output-relative image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an output folder, copy referenced source images into an images/ directory, and relink image paths for the generated deck.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
