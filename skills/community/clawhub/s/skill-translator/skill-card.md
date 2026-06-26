## Description: <br>
Translates an existing SKILL.md document into Chinese while preserving Markdown structure and most YAML frontmatter, then writes the translation as SKILL(1).md in the same directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to produce a Chinese translation of a SKILL.md file for review, localization, or sharing with Chinese-speaking users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads from a user-provided path, so an incorrect path could translate the wrong SKILL.md file. <br>
Mitigation: Confirm the target directory is the intended skill directory before running the translation. <br>
Risk: The skill may overwrite an existing SKILL(1).md file in the target directory. <br>
Mitigation: Check for an existing SKILL(1).md and preserve any prior translation or manual edits before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JEyeshield/skill-translator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SKILL(1).md beside the source SKILL.md and may overwrite an existing file with that name.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
