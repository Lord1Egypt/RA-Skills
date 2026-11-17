## Description:

Researches RedNote/Xiaohongshu community signals through public-web review, optional user-approved login-enhanced browser review, query expansion, claim extraction, and concise evidence-aware reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pippin1214](https://clawhub.ai/user/pippin1214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research RedNote/Xiaohongshu reputation, trends, controversies, local recommendations, creator activity, and multimodal discussion clues while keeping uncertainty and access limits visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private screenshots, chat logs, copied comments, subtitles, or OCR text may be turned into public search queries.

Mitigation: Ask the user to crop or redact personal identifiers before providing sensitive material and show proposed external search terms before running them.

Risk: Login-enhanced review may expose privacy-sensitive account or session content beyond the immediate research need.

Mitigation: Use login only after explicit user opt-in, rely on site-native login flows, keep collection task-scoped, and avoid unrelated browsing or actions.

Risk: Public-web RedNote evidence can be thin, delayed, snippet-only, or blocked, leading to overconfident conclusions.

Mitigation: State the access mode, separate direct evidence from rumor or repeated anecdote, and mark conclusions inconclusive when evidence remains weak.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pippin1214/skills/rednote-research)
- [RedNote Access Modes](references/access-modes.md)
- [Login-Enhanced Workflow](references/login-enhanced-workflow.md)
- [Minimal User Input Paths](references/minimal-user-input-paths.md)
- [Account Summary Templates](references/account-summary-template.md)
- [RedNote Structured Claim Log](references/claim-log-schema.md)
- [RedNote Multimodal Capture Patterns](references/multimodal-capture.md)
- [RedNote Community Intelligence Output Patterns](references/output-patterns.md)
- [RedNote Public-Web Recovery Patterns](references/public-web-recovery.md)
- [RedNote Community Intelligence Scoring Rubric](references/scoring-rubric.md)
- [RedNote Community Intelligence Verification Patterns](references/verification-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, structured claim logs, JSON templates, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify whether evidence came from public-web mode or login-enhanced review and should label uncertain, snippet-only, or partially inspectable media claims.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
