## Description: <br>
Accepts a topic or source material such as reports, data, copy, or PPTX files, then helps an agent turn the material into Slidev Markdown and previewable HTML slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfewsuper](https://clawhub.ai/user/sfewsuper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert topics, documents, data, web content, or existing presentations into Slidev-based slide decks that can be previewed and exported. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read user-provided files, URLs, reports, data, or presentations while preparing a slide deck. <br>
Mitigation: Use a dedicated project folder and avoid confidential documents or internal URLs unless the execution environment is trusted. <br>
Risk: The skill may install npm dependencies, run npx commands, export slides, or start a Slidev preview. <br>
Mitigation: Require explicit approval before npm install, npx, export, or --remote preview steps. <br>
Risk: The skill may modify files in the working directory while creating Slidev project assets. <br>
Mitigation: Run it in a clean or disposable workspace and review generated files before reuse or publication. <br>


## Reference(s): <br>
- [Slidev Assist Quick Reference](references/quickref.md) <br>
- [Slidev Documentation](https://sli.dev) <br>
- [Slidev Getting Started](https://github.com/slidevjs/slidev#getting-started) <br>
- [ClawHub Release Page](https://clawhub.ai/sfewsuper/slidev-assist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown slides, Slidev frontmatter, command snippets, and presentation workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify project files, install npm dependencies, start a local Slidev preview, and export slides to PDF, PPTX, or PNG when approved.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
