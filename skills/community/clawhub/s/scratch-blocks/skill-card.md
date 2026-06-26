## Description: <br>
Use this skill when the user uploads a `.sb3` or `.sprite3` file, or when the conversation is about Scratch and clearer block-style visualization would help. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-bra0](https://clawhub.ai/user/z-bra0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and Scratch users use this skill to inspect Scratch project or sprite files, reason over extracted Scratch block structures, and present Scratch code as readable rendered ASCII blocks instead of raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local extraction and rendering can leave generated Scratch data in /tmp/scratchcode or beside raw JSON inputs. <br>
Mitigation: Delete generated scratch-json and rendered-output files after use when retained local copies are not desired. <br>


## Reference(s): <br>
- [Scratch Blocks on ClawHub](https://clawhub.ai/z-bra0/scratch-blocks) <br>
- [Uploaded Scratch Files](references/UPLOADS.md) <br>
- [Block Catalog Spec](data/BLOCK_CATALOG_SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with fenced ASCII-rendered Scratch blocks and concise explanatory prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts to extract Scratch files into scratch-json and render Scratch blocks for display; scratch-json is an internal intermediate format.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
