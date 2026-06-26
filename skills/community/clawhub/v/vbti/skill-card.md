## Description: <br>
VBTI analyzes local Claude coding transcripts, classifies the user into one of 16 playful vibe-coder types, and generates a shareable HTML diagnostic card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinadu-ai](https://clawhub.ai/user/tinadu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and vibe-coding tool users run this skill to summarize their local Claude coding-session history into a novelty personality-style classification and HTML card. It is intended for local analysis and optional sharing after the user reviews the generated report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly analyzes private Claude transcript history, including prompts, pasted tool results, command patterns, file paths, and timing metadata. <br>
Mitigation: Run it only when the user is comfortable with local transcript analysis, and review the source behavior before installing or executing it. <br>
Risk: The generated Desktop HTML report may contain sensitive or identifying information derived from local coding history. <br>
Mitigation: Inspect the generated HTML card before sharing screenshots or the file publicly. <br>
Risk: Opening the generated HTML may contact Google Fonts through the browser. <br>
Mitigation: Open the file with network access disabled or replace remote font imports when external font requests are not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tinadu-ai/vbti) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill manifest](artifact/SKILL.md) <br>
- [Type definitions](artifact/vbti_types.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Console text plus a generated HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the diagnostic card to the user's Desktop and attempts to open it in a browser.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
