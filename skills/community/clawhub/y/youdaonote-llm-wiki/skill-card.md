## Description:

YoudaoNote LLM Wiki helps an agent create, maintain, query, lint, and archive a persistent LLM-style knowledge base in YoudaoNote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lephix](https://clawhub.ai/user/lephix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YoudaoNote into a structured wiki for research notes, source ingestion, cross-linked summaries, archived conversations, and consistency checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write persistent YoudaoNote wiki content.

Mitigation: Use it only for accounts and workspaces where agent access to wiki content is acceptable, and review proposed changes before write operations.

Risk: Archived notes may contain secrets, credentials, personal identifiers, or sensitive business content.

Mitigation: Ask the agent to show exactly what will be saved before archiving and remove sensitive content before writing notes.

Risk: The release evidence flags an unverified remote installer command and recommends caution.

Mitigation: Prefer a verified YoudaoNote CLI installation path and review installer contents before running curl-to-bash commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lephix/skills/youdaonote-llm-wiki)
- [YoudaoNote homepage](https://note.youdao.com)
- [YoudaoNote CLI install guide](https://note.youdao.com/help-center/cli-install-guide.html)
- [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with YoudaoNote CLI commands and note content guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update cloud note folders and Markdown notes through the YoudaoNote CLI.]

## Skill Version(s):

1.0.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
