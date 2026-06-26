## Description: <br>
语文写作教练 is a Chinese-language writing coach that guides students through brainstorming, logic checks, self-drafting, targeted feedback, revision, writing-style tracking, genre-specific coaching, Socratic questioning, and debate practice without writing the essay for them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students and families use this skill to develop Chinese composition and argumentation skills through guided questions, rubric-based critique, debate practice, and revision coaching while preserving the student's own wording and style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional writing-style profile may store patterns from student writing over time. <br>
Mitigation: Enable the style-DNA feature only after the student or guardian understands what is stored and how to opt out or clear it. <br>
Risk: Draft workflow recovery may rely on local memory for unfinished writing sessions. <br>
Mitigation: Avoid using recovery memory for sensitive student writing unless local retention is acceptable. <br>
Risk: The skill is designed for coaching and may be misused to request ghostwritten essay content. <br>
Mitigation: Follow the artifact's stated behavior of refusing to write sentences, paragraphs, openings, endings, or complete essays for the student. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qizhitang/xiaozhi-chinese-writing-coach) <br>
- [writing-5step-statemachine.md](references/writing-5step-statemachine.md) <br>
- [writing-rubric.md](references/writing-rubric.md) <br>
- [debate-script-guide.md](references/debate-script-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversational coaching with structured feedback, questions, rubrics, and revision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain an optional local writing-style profile only with user consent.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter is 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
