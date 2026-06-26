## Description: <br>
Skill Refiner audits OpenClaw skill files by scoring SKILL.md quality, validating frontmatter and references, optionally checking links, and producing a read-only Markdown review log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crispyangles](https://clawhub.ai/user/Crispyangles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review OpenClaw skill files for quality, broken references, frontmatter issues, untagged code blocks, and optional link freshness before release or during recurring maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional link freshness checks can contact every URL present in reviewed SKILL.md files. <br>
Mitigation: Run the optional link check only when those outbound requests are acceptable for the workspace being audited. <br>
Risk: The saved review log may include details from private or sensitive skill content. <br>
Mitigation: Review the generated memory log before sharing or publishing it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Crispyangles/sparkforge-skill-refiner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review log with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only review workflow; optional link checking may contact URLs found in SKILL.md files.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
