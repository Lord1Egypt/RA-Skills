## Description: <br>
Personal knowledge wiki managed by your agent. Create, link, search articles. Build a searchable knowledge base through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to maintain a local personal knowledge wiki through an agent, including creating articles, linking related topics, searching notes, and exporting wiki content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and overwrites local Markdown files in its wiki folder, which could replace prior notes if used carelessly. <br>
Mitigation: Use a dedicated wiki folder, review agent changes, and keep independent backups of important notes. <br>
Risk: Personal or sensitive information added to the wiki is persisted on disk. <br>
Mitigation: Avoid storing passwords, tokens, or highly sensitive material unless the local storage location is intentionally secured. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/wiki-local) <br>
- [README](README.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown articles and plain-text search, backlink, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local Markdown files and a JSON index under the configured wiki folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
