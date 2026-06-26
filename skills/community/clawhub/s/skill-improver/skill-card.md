## Description: <br>
This skill reviews and improves OpenClaw SKILL.md files against a bundled quality standard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phallusophy](https://clawhub.ai/user/phallusophy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to audit OpenClaw SKILL.md files, grade them against the included quality standard, and generate improvement suggestions or an optimized SKILL.md when issues are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be asked to inspect private or unrelated files when locating a target SKILL.md. <br>
Mitigation: Limit inputs to the intended SKILL.md or skill directory and avoid providing paths that expose private or unrelated content. <br>
Risk: Suggested rewrites may introduce incorrect or misleading guidance into a skill. <br>
Mitigation: Review generated edits before applying them and scan the revised skill before release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/phallusophy/skill-improver) <br>
- [Skill Reviewer](skill-reviewer/skill-reviewer.md) <br>
- [OpenClaw Skill Quality Standard](skill-standard/skill-standard.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, guidance] <br>
**Output Format:** [Markdown reports with optional optimized SKILL.md code blocks and JSON-shaped status examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include grades, issue counts, dimension scores, suggested fixes, and failure details for parse or file errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill-reviewer frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
