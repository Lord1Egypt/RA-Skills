## Description: <br>
Russian Humanizer helps agents detect and remove AI-style cliches, bureaucratic phrasing, artificial structure, and unnatural constructions from Russian-language text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Horosheff](https://clawhub.ai/user/Horosheff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and agents use this skill to review Russian text for AI-style filler, rhythm problems, stock phrases, and rigid structures, then rewrite or clean the text into a more natural form. It is most useful when preparing Russian prose, marketing copy, documentation, or assistant-generated drafts for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Glavred analyzer can send the full submitted text to glvrd.ru. <br>
Mitigation: Use the local analyzer and auto-fix tools for confidential text; use the Glavred check only when external submission is acceptable. <br>
Risk: The bundled anti-slop prompt can broadly change an assistant's Russian writing style if installed as a global instruction. <br>
Mitigation: Apply the prompt only in contexts where this stricter editing style is desired, or scope it to the specific writing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Horosheff/russian-humanizer) <br>
- [Phrases reference](references/phrases.md) <br>
- [Structures reference](references/structures.md) <br>
- [Examples reference](references/examples.md) <br>
- [Glavred service](https://glvrd.ru) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Plain text or Markdown reports with detected phrases, scoring, rewrite guidance, and optional cleaned text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional Glavred analyzer sends submitted text to glvrd.ru; the local analyzer and auto-fix paths can be used without that external submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
