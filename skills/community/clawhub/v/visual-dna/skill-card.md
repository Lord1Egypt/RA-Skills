## Description: <br>
Extract visual identity into reusable Design DNA JSON, then apply it to generate faithful UI from references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and designers use this skill to extract reusable visual identity profiles from screenshots, images, or URLs, then apply those profiles to generate matching UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may analyze private screenshots, internal URLs, authenticated pages, regulated data, or third-party designs when users provide them as references. <br>
Mitigation: Use only references the user is authorized to analyze, avoid sensitive or regulated inputs, and review generated Design DNA before committing or sharing it. <br>
Risk: Generated Design DNA or UI can reflect inaccurate or unauthorized interpretations of a visual reference. <br>
Mitigation: Report the references used, review the extracted profile against the source, and ask for clarification when a reference is ambiguous, unavailable, or requires credentials. <br>


## Reference(s): <br>
- [Design DNA Schema](references/schema.md) <br>
- [Generation Guide](references/generation-guide.md) <br>
- [Sample Design DNA JSON](examples/sample-design-dna.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/visual-dna) <br>
- [Inspired Design DNA Repository](https://github.com/zanwei/design-dna) <br>
- [No Slop UI Pairing](https://github.com/LeoStehlik/no-slop-ui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, guidance] <br>
**Output Format:** [Design DNA JSON, Markdown guidance, and self-contained HTML/CSS/JS code when generating UI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports which references were used and asks before generation after analysis.] <br>

## Skill Version(s): <br>
0.2.2 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
