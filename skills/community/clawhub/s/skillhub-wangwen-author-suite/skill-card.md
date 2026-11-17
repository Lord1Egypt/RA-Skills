## Description:

Wangwen Author Suite helps agents support Chinese web-novel authors with guided story starts, outline-first planning, Tomato-platform writing workflows, title and blurb drafting, chapter review, prose cleanup, and Markdown-to-TXT export guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[code-hermit-tao](https://clawhub.ai/user/code-hermit-tao)

### License/Terms of Use:

MIT-0

## Use Case:

External authors and writing assistants use this skill to plan, draft, review, and package Chinese serialized web fiction. It is especially oriented toward Tomato-style chapter workflows, quality checks, launch copy, and export of chapter Markdown into plain TXT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TXT export workflow can remove existing .txt files from the selected output directory.

Mitigation: Use a dedicated empty export folder under the relevant novels/book directory, back it up before export, and require explicit confirmation before running the export command.

Risk: Generated chapters, reviews, and platform guidance may be treated as publication-ready without human judgment.

Mitigation: Require author review of quality scores, platform-sensitive content, originality, and final publication decisions; the skill itself states that it does not guarantee ranking, platform review, or algorithmic success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/code-hermit-tao/skills/skillhub-wangwen-author-suite)
- [README](README.md)
- [Usage examples](examples.md)
- [Quality hard standards](references/quality-hard-standards.md)
- [Tomato workflow details](references/tomato-line.md)
- [Tomato quality checklist](references/tomato-quality-checklist.md)
- [Built-in reviewer rubric](references/juzu-reviewer.md)
- [Fanqie export guidance](references/export-fanqie.md)
- [Platform gate guidance](references/platform-gate.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with structured checklists, tables, code blocks, optional shell commands, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create files under a novels/book folder and may provide Python export commands for Markdown-to-TXT conversion.]

## Skill Version(s):

1.0.1 (source: server release evidence, PUBLISH.md, README.md, TRACE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
