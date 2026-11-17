## Description:

Publish Knowledge Health Checker diagnoses Markdown-style knowledge bases by finding placeholder files, broken wiki links, content-density issues, and weak note-network structure, then produces reports and repair guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xb19960921](https://clawhub.ai/user/xb19960921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to scan Obsidian, Notion exports, Logseq, and Markdown repositories for empty notes, broken links, weak structure, and isolated content before cleanup or migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated repair scripts can delete or rewrite knowledge-base files.

Mitigation: Back up the knowledge base and manually inspect generated auto-fix scripts before running them.

Risk: Scheduled checks or notification delivery can create persistent recurring activity.

Mitigation: Enable cron, email, or Feishu delivery only when persistent scheduled runs are explicitly desired.

Risk: Generated HTML reports may expose local file paths or repository structure.

Mitigation: Treat reports as local review artifacts and remove sensitive path details before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xb19960921/skills/publish-knowledge-health-checker)
- [Code review report](artifact/code-review-report.md)
- [Final evaluation report](artifact/final-evaluation.md)
- [Test prompts](artifact/test-prompts.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell and Python snippets, plus generated HTML reports or repair scripts when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files such as health-report-*.html and auto-fix scripts; review generated repair actions before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
