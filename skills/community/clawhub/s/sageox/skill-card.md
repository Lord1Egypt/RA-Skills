## Description:

SageOx helps agents query team knowledge, manage AI coworkers, distill and summarize activity, catch up on recent work, and import or export knowledge across configured repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avi-ox-agola](https://clawhub.ai/user/avi-ox-agola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team members use SageOx inside coding-agent sessions to search team context, load expert coworker prompts, generate summaries, run distillation workflows, and bridge knowledge into or out of SageOx.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install local tooling and depends on the SageOx ox release path.

Mitigation: Review the bundled install flow before use and install only when the publisher and pinned ox release path are trusted.

Risk: Summaries, catchups, imports, and video processing may send private team content to external services.

Mitigation: Use only with data approved for those services, and avoid running import or synthesis workflows on sensitive repositories without organizational approval.

Risk: The skill can read and persist team and repository memory in shared local state files.

Mitigation: Review configured repositories and state files before execution, and remove stale or unauthorized team entries.

Risk: Team-managed coworker prompts can be loaded into the active agent session.

Mitigation: Load coworker prompts only from trusted teams and inspect unfamiliar prompts before applying their guidance.

## Reference(s):

- [SageOx homepage](https://sageox.ai)
- [ClawHub Sageox listing](https://clawhub.ai/avi-ox-agola/skills/sageox)
- [Setup](references/setup.md)
- [Query](references/query.md)
- [Coworkers](references/coworkers.md)
- [Distill](references/distill.md)
- [Distill Pipeline](references/distill-pipeline.md)
- [Summary](references/summary.md)
- [Glance](references/glance.md)
- [Catchup](references/catchup.md)
- [Import/Export](references/import-export.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows can write local state files, invoke command-line tools, or call Claude for synthesis after prerequisites are verified.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
