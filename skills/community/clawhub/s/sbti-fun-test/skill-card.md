## Description:

Runs a Chinese-language SBTI entertainment personality quiz with 30 questions, four answer choices, humorous personality results, and ASCII-art pets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

External users or developers use this skill to run or embed a local entertainment-only SBTI personality quiz and produce a humorous result summary. It should not be used for diagnosis, hiring, relationship decisions, or other consequential assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake humorous personality results for diagnostic or decision-grade assessment.

Mitigation: Present and use the quiz as entertainment only, and do not rely on it for diagnosis, hiring, relationship, or other consequential decisions.

Risk: Older V1/V2 scripts are bundled beside the current V3 entrypoint.

Mitigation: Use the documented scripts/sbti_test.py entrypoint for the current release unless intentionally reviewing legacy behavior.

Risk: Documentation may overstate the exact V3 result count.

Mitigation: Treat the quiz output as the authoritative runtime result and avoid making precise governance claims from the advertised count alone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laojun509/skills/sbti-fun-test)
- [Publisher profile](https://clawhub.ai/user/laojun509)
- [Original author profile](https://space.bilibili.com/417038183)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Terminal text or Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces entertainment quiz prompts, formatted personality summaries, dimension analysis, and ASCII-art result displays.]

## Skill Version(s):

3.0.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
