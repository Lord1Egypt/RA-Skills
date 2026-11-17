## Description:

Xuanhuan Novelist helps agents plan, write, continue, polish, and validate long-form Chinese xuanhuan and cultivation novels with structured worldbuilding, cultivation systems, chapter plans, and word-count checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoheorg](https://clawhub.ai/user/xiaoheorg)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agent users use this skill to create or continue Chinese fantasy novels across 10-50 chapters, including setup, outline generation, chapter drafting, style matching, polishing, and validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically scan, write, rewrite, and run commands on many workspace files with weak path and consent boundaries.

Mitigation: Use a dedicated empty project folder, confirm the output path before generation, and review generated titles and plan paths for unsafe characters.

Risk: Parallel writing, agent-team modes, and automatic repair can create or modify many chapters before the user reviews them.

Mitigation: Prefer serial mode for first runs, monitor bulk-writing modes, and inspect generated plans and file changes before relying on the output.

Risk: Draft analysis may read unrelated writing if pointed at a broad workspace.

Mitigation: Provide a specific draft folder or file set and avoid running analysis from a workspace that contains unrelated drafts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoheorg/skills/xuanhuan-novelist)
- [Cultivation System Guide](references/guides/cultivation-system.md)
- [Xuanhuan Worldbuilding Guide](references/guides/xuanhuan-worldbuilding.md)
- [Xuanhuan Plot Patterns](references/guides/xuanhuan-plot-patterns.md)
- [Battle Writing Guide](references/guides/battle-writing.md)
- [Chapter Writing Guide](references/guides/chapter-guide.md)
- [Content Expansion Guide](references/guides/content-expansion.md)
- [Phase 2 Planning Flow](references/flows/phase2-planning.md)
- [Phase 3 Writing Flow](references/flows/phase3-writing.md)
- [Phase 4 Validation Flow](references/flows/phase4-validation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown novel chapters and planning files, JSON writing plans, and occasional shell commands for word-count validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and edits multiple files in a chosen workspace; optional parallel and agent-team modes can increase change volume.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
