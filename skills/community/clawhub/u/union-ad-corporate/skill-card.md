## Description: <br>
UnionSkill enterprise blue advertising PPT skill for turning documents, notes, or text prompts into branded business presentation assets through outline confirmation, slide image generation, and PPTX assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and business teams use this skill to create UnionSkill-branded corporate blue presentations for B2B proposals, annual reports, roadshows, trade shows, and customer pitches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated slides may include incorrect text, unreadable Chinese headings, or unwanted visual artifacts from the image generation step. <br>
Mitigation: Confirm the outline before generation and perform the documented QA checks for slide count, blank pages, readable Chinese titles, and brand watermark placement before delivery. <br>
Risk: The security review summary is clean, but the provided security guidance calls for careful confirmation before sensitive maintainer-style workflows. <br>
Mitigation: Confirm the target, reason, dry-run output, backup status, and apply gate before using any workflow that can affect an operational environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/union-ad-corporate) <br>
- [Publisher profile](https://clawhub.ai/user/timo2026) <br>
- [README.md](README.md) <br>
- [Enterprise business style guide](references/style_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with bash commands, file paths, and delivery notes for PPTX, image ZIP, text, and optional HTML outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation of the slide outline before image generation; generated slide images are assembled into a UnionSkill-branded PPTX with watermark, closing page, and metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
