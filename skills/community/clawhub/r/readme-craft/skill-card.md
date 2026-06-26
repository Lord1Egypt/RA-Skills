## Description: <br>
README Craft helps agents create, audit, and rewrite project README files using a 22-item quality rubric and practical README patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to draft a new README, audit an existing README, or rewrite outdated README content for open-source or internal projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: README drafts or rewrites can introduce inaccurate, outdated, or misleading project guidance. <br>
Mitigation: Use audit mode for read-only review when appropriate, and inspect generated diffs before accepting rewrite changes. <br>
Risk: Shell, web fetch, or delegated-agent actions may be requested during README generation. <br>
Mitigation: Approve only actions that are clearly tied to README creation, auditing, or rewriting. <br>


## Reference(s): <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>
- [Badge and Visuals](references/badge-and-visuals.md) <br>
- [Community Standards](references/community-standards.md) <br>
- [Real-World Patterns](references/real-world-patterns.md) <br>
- [Oh My Claude Code README](https://github.com/Yeachan-Heo/oh-my-claudecode) <br>
- [Everything Claude Code README](https://github.com/affaan-m/everything-claude-code) <br>
- [Awesome README](https://github.com/matiassingers/awesome-readme) <br>
- [Standard README](https://github.com/RichardLitt/standard-readme) <br>
- [Art of README](https://github.com/hackergrrl/art-of-readme) <br>
- [Make a README](https://makeareadme.com/) <br>
- [How to Write a Great README](https://thoughtbot.com/blog/how-to-write-a-great-readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, README files, README diffs, and inline code or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Create and rewrite modes may write README.md after review; audit mode reports scores and recommendations without file changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
