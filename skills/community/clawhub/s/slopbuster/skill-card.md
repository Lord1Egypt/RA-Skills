## Description: <br>
Slopbuster helps agents detect, score, and rewrite AI-patterned prose, code comments, commit messages, docstrings, and academic writing while preserving meaning and adding a more human voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, developers, editors, and academic authors use this skill to clean up AI-generated phrasing, comments, naming, commit messages, docstrings, and papers. It supports quick, standard, and deep passes with scoring, two-pass review, and optional voice calibration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional setup instructions can make the skill's writing style rules persist across future agent replies, comments, documentation, and commit messages. <br>
Mitigation: Keep persistent setup project-scoped when possible, and review global agent instructions before applying them. <br>
Risk: Rewrite and file-edit modes can change wording, tone, or code-adjacent text in ways the user did not intend. <br>
Mitigation: Review proposed edits and saved files before accepting them, especially for public, academic, legal, or production-facing content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/slopbuster) <br>
- [Setup guide](docs/setup-guide.md) <br>
- [Voice and soul guide](guides/voice-and-soul.md) <br>
- [Scoring system](scoring.md) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with rewritten text, score summaries, change lists, code suggestions, and optional edited files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save rewritten files when file-editing tools are used; score-only mode returns analysis without rewriting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, CHANGELOG.md released 2026-03-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
