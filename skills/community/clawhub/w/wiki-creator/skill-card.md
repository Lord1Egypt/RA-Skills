## Description: <br>
Builds and maintains a persistent Markdown knowledge wiki from uploaded documents, with wiki-first querying, two-level indexes, source-cited pages, and no vector retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuhanli](https://clawhub.ai/user/neuhanli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to convert uploaded documents into a structured local or global Markdown wiki, maintain it over time, and answer knowledge questions from the wiki before using web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents are copied into a persistent .wiki-creator directory and may be reused automatically in later wiki queries. <br>
Mitigation: Use an explicit project-local root for sensitive material, confirm where the wiki is stored, add the directory to .gitignore when appropriate, and delete raw files or generated wiki data when they should no longer be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neuhanli/skills/wiki-creator) <br>
- [Query Mode](references/query-mode.md) <br>
- [Page Authoring](references/page-authoring.md) <br>
- [Schema Guide](references/schema-guide.md) <br>
- [Cascade Update](references/cascade-update.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, generated wiki files, JSON script output, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates persistent .wiki-creator wiki data in a project-local or user-global directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; changelog source: user) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
