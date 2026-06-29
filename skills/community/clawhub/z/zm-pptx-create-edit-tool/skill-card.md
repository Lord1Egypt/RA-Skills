## Description: <br>
ZM PPTX 创建与编辑工具 helps agents create, inspect, and edit Microsoft PowerPoint/PPTX decks, including layouts, templates, placeholders, notes, charts, and basic visual QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and presentation authors use this skill when a task requires creating, checking, or editing PPTX decks while preserving template structure, layout fidelity, notes, comments, charts, and final visual quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read or modify user-provided presentation files, including notes, comments, media, templates, and charts. <br>
Mitigation: Review generated or edited decks before formal use, and verify affected slides, notes, comments, media, templates, and charts. <br>
Risk: Layout, placeholder, font, image, or chart changes can make a deck look correct in text inspection but fail visually. <br>
Mitigation: Open, parse, or render the resulting PPTX and perform a visual QA pass before delivery. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jerryxn/skills/zm-pptx-create-edit-tool) <br>
- [Skill homepage](https://clawic.com/skills/zm-pptx-create-edit-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown instructions and status summaries, with PPTX files created or modified when the agent executes the workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final responses should use PASS, NEEDS_REVISION, or BLOCKED and explain the result.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
