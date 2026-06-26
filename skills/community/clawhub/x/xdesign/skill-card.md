## Description: <br>
XDesign routes visual design requests into workflows for HTML slide decks, interactive prototypes, animations, design systems, and presentation exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qomob](https://clawhub.ai/user/qomob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, product teams, and other external users use this skill to turn visual requests, documents, brand references, or rough ideas into presentable HTML decks, UI prototypes, animations, design-system notes, and export-ready presentation assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language can make the skill engage on ambiguous visual-design prompts. <br>
Mitigation: Confirm the intended mode and scope before acting when the request is vague or could map to multiple visual deliverables. <br>
Risk: Design requests may involve private repositories, internal assets, or sensitive brand materials. <br>
Mitigation: Use only materials the user is authorized to share and avoid including private or internal assets in generated public artifacts. <br>
Risk: Generated HTML may load fonts or JavaScript from third-party CDNs. <br>
Mitigation: Vendor external resources locally or review network dependencies before deploying or sharing generated HTML in controlled environments. <br>


## Reference(s): <br>
- [XDesign README](artifact/README.md) <br>
- [XDesign Skill Definition](artifact/SKILL.md) <br>
- [Workflow Guide](artifact/references/workflow-guide.md) <br>
- [Technical Specifications](artifact/references/technical-specs.md) <br>
- [Mode 2 Prototype Workflow](artifact/references/mode-2-prototype.md) <br>
- [Deck Studio Catalog](artifact/references/deck-studio-catalog.md) <br>
- [Design System Catalog](artifact/references/design-system-catalog.md) <br>
- [HTML PPT Skill](https://github.com/lewislulu/html-ppt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, React, shell snippets, and generated artifact files such as standalone HTML, PPTX, PDF, PNG, or design-system notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce single-file HTML or self-contained directories; some outputs may rely on browser rendering, CDN resources, or export helpers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
