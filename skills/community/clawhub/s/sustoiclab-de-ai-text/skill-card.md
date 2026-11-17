## Description:

A Chinese text-polishing skill that removes AI-like style while preserving the original meaning, facts, and paragraph structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[susstoiclab](https://clawhub.ai/user/susstoiclab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and editors use this skill to polish Chinese drafts, review manuscripts, and reduce AI-like phrasing without adding information or changing the source meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad editing, review, or proofreading requests when the user only wants ordinary proofreading.

Mitigation: Ask the user whether they want de-AI-style rewriting or basic proofreading when the requested editing posture is ambiguous.

Risk: Style rewriting can unintentionally alter nuance even when facts are preserved.

Mitigation: Keep edits limited to language and style, preserve the source meaning and paragraph structure, and avoid adding information.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/SusStoicLab/Su-s-Stoic-Lab/tree/main/sustoiclab-de-ai-text)
- [ClawHub skill page](https://clawhub.ai/susstoiclab/skills/sustoiclab-de-ai-text)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text preserving the original paragraph structure; an editor note may be added only when special context requires explanation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to output only the revised text and avoid extra explanation in normal use.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
