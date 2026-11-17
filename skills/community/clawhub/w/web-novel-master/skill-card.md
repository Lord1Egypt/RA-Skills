## Description:

Web Novel Master helps agents plan, draft, polish, and validate Chinese web-novel projects across Fast, Professional, and Industrial writing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinylion1024](https://clawhub.ai/user/tinylion1024)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, creative teams, and agent users use this skill to structure, draft, revise, and quality-check serial web fiction in genres such as urban power fantasy, cultivation fantasy, rebirth, and romance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project file creation can escape the intended project folder if a project name contains path characters.

Mitigation: Use a disposable workspace, sanitize project names, reject slashes, backslashes, absolute paths, and .. components, and confirm any write outside ./web-novels/.

Risk: Industrial mode can run multi-agent drafting without repeated confirmation.

Mitigation: Require explicit user confirmation before enabling Industrial mode or multi-agent drafting, and review generated tasks and files before continuing.

## Reference(s):

- [Web Novel Master README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Mode Selector](artifact/references/flows/Mode_Selector.md)
- [Shared Infrastructure](artifact/references/flows/Shared_Infrastructure.md)
- [Chapter Writing Guide](artifact/references/guides/Chapter-Writing-Guide.md)
- [Opening Formula](artifact/references/Plot/Opening-Formula.md)
- [Excitement Point Guide](artifact/references/Plot/Excitement-Point-Guide.md)
- [Chapter Word Count Script](artifact/scripts/check_chapter_wordcount.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with optional JSON project metadata and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local writing project files, including project plans and chapter drafts.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
