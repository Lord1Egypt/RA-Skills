## Description: <br>
Turns ideas, outlines, documents, or drafts into structured, polished enterprise-grade HTML presentations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feeicn](https://clawhub.ai/user/feeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external presenters, and developers can use this skill to turn topics, drafts, outlines, speech notes, or existing HTML slides into branded standalone HTML presentation decks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently update its local checkout before use. <br>
Mitigation: Review or disable the automatic git pull step and pin a reviewed release before installation or execution. <br>
Risk: The artifact bundles an unrelated Sonos-control skill. <br>
Mitigation: Remove the unrelated skills/sonoscli directory from the release or review it separately before deployment. <br>
Risk: Some example decks may load external fonts when opened. <br>
Mitigation: Open examples in an approved network environment or remove external font loading from retained examples. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/feeicn/slide-writer) <br>
- [Project Homepage](https://github.com/FeeiCN/slide-writer) <br>
- [Live Demo](https://feei.cn/slide-writer/examples/) <br>
- [README](README.md) <br>
- [Testing Notes](TESTING.md) <br>
- [Component Library](components.md) <br>
- [Theme Index](themes/_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and standalone HTML presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks are intended as single-file HTML with inline CSS and JavaScript.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
