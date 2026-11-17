## Description:

Rewrites existing Chinese text with an AI-like tone using register-aware edits and semantic checks intended to preserve facts and meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songzhou666](https://clawhub.ai/user/songzhou666)

### License/Terms of Use:

MIT-0

## Use Case:

People revising existing AI-generated or AI-like Chinese prose use the skill to make targeted register-aware edits and review whether facts, positions, and meaning were preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Required searches can expose details from the source text.

Mitigation: Keep confidential text out of external searches unless sanitized queries are explicitly approved.

Risk: Revisions and automated checks may miss changes to facts or meaning.

Mitigation: Manually verify facts, numbers, and negations against the original text even when checks pass.

Risk: Saved drafts and style profiles may retain sensitive writing.

Mitigation: Review or remove saved drafts and profiles under .agent/harness/ when finished.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/songzhou666/sz-ink)
- [ClawHub skill release](https://clawhub.ai/songzhou666/skills/sz-ink)
- [blader/humanizer (referenced lexicon research)](https://github.com/blader/humanizer)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Rewritten Chinese text with Markdown metrics, change, and semantic review reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works on existing text; a factual follow-up list may be included when source material lacks required experience details.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter lists 0.4.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
