## Description:

Breaks a provided script into a shootable shot list with concrete visuals, framing, movement, timing, subtitles, props, total duration, shooting difficulty, and lower-complexity alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to turn Chinese voiceover or story scripts into practical Markdown shot lists for short videos. It helps plan camera setup, aspect ratio, timing, visual coverage, subtitles, props, difficulty, and lower-resource alternatives before filming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad filming-related trigger phrases may activate the skill for general filming questions.

Mitigation: Confirm that the user wants a script-to-shot-list workflow, and ask for the desired output language when it is not clear.

Risk: Shot timing and shooting difficulty are planning estimates and may not match the final filmed result.

Mitigation: Review the generated shot list against the actual script length, speaking speed, location, equipment, and production constraints before filming.

Risk: The skill produces planning text only and does not create video, images, edits, or media assets.

Mitigation: Use the Markdown output as a filming plan and route media creation or editing work to appropriate production tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyuming0823/skills/ym-script-to-shotlist)
- [Source Repository](https://github.com/liuyuming0823/ym-script-to-shotlist)
- [Framing and Movement Guide](references/framing-movement.md)
- [Shot List Template](templates/shotlist-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown shot list with tables and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes filming assumptions, a seven-column shot table, duration estimates, difficulty and cost notes, and a lower-complexity version; does not generate video or image files.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
