## Description: <br>
Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keylimesoda](https://clawhub.ai/user/keylimesoda) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to turn technical concepts, architecture, code reviews, plans, recaps, comparisons, and data tables into visual HTML explanations and slide decks for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated explanations may include incorrect or misleading technical claims when source context is incomplete. <br>
Mitigation: Review generated diagrams, summaries, and slide decks against the source project before relying on or sharing them. <br>
Risk: The share workflow can publish selected HTML pages publicly through Vercel. <br>
Mitigation: Do not use the share workflow for confidential code, architecture, plans, customer data, or other sensitive content. <br>
Risk: The fact-check workflow can edit documents in place. <br>
Mitigation: Review resulting diffs before accepting corrections or using the edited document as authoritative. <br>
Risk: The skill can write persistent HTML files, open them in a browser, and optionally use external image-generation tools. <br>
Mitigation: Inspect generated files and avoid sending sensitive content to optional external tooling. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/keylimesoda/visual-explainer-openclaw) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [CSS Patterns](references/css-patterns.md) <br>
- [Libraries](references/libraries.md) <br>
- [Responsive Navigation](references/responsive-nav.md) <br>
- [Slide Patterns](references/slide-patterns.md) <br>
- [Share Workflow](prompts/share.md) <br>
- [Fact Check Workflow](prompts/fact-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated self-contained HTML, shell commands, and file edits when workflows request them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is intended to be opened locally in a browser; the share workflow can publish selected HTML pages publicly through Vercel.] <br>

## Skill Version(s): <br>
0.5.1-openclaw.1 (source: ClawHub release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
