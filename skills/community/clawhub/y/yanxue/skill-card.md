## Description: <br>
Yanxue generates and manages study-trip course plans by city, grade band, destination, theme, and duration, with support for Markdown saving and Word export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dmeteor8](https://clawhub.ai/user/Dmeteor8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Educators, study-trip mentors, and education service teams use this skill to draft, manage, and export structured study-trip curriculum plans for primary and secondary school learners. <br>

### Deployment Geography for Use: <br>
Global; bundled destination examples focus on Jiangsu, Zhejiang, Shanghai, and nearby Chinese cities. <br>

## Known Risks and Mitigations: <br>
Risk: The save helper can write outside the advertised course folder if course names include path components. <br>
Mitigation: Use simple course names without slashes, absolute paths, or '..', and verify the saved path before sharing or reusing generated files. <br>
Risk: Generated materials may be used with minors and may include unsuitable, unsafe, or age-inappropriate course content. <br>
Mitigation: Review generated plans for safety, neutrality, accuracy, and age appropriateness before distributing them to students or educators. <br>
Risk: Word export depends on local Python packages and converts user-provided Markdown files. <br>
Mitigation: Install dependencies only from trusted sources and verify input and output file paths before running export commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Dmeteor8/yanxue) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Course Plan Template](artifact/templates/template.md) <br>
- [Recommended Study-Trip Destination Library](artifact/references/destinations.md) <br>
- [Study-Trip Policy Background](artifact/references/policy-background.md) <br>
- [User Case Style Guide](artifact/references/style-guide.md) <br>
- [Example Study-Trip Course Plan](artifact/references/example-course.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown course plans, optional DOCX exports, and shell commands for save/export helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save Markdown course files under /home/ubuntu/yanxue_courses and convert Markdown inputs to DOCX when Python dependencies are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
