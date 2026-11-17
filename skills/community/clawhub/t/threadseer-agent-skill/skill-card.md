## Description:

Threadseer transforms transcripts, meetings, chats, interviews, voice notes, and mixed conversational material into evidence-backed decision briefs, recommendations, action plans, risk and insight analyses, shareable team reports, follow-up drafts, and institutional memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers, knowledge workers, and teams use Threadseer to convert supplied conversations into evidence-backed decision briefs, action plans, risk and insight analyses, follow-up drafts, and durable memory while separating explicit evidence from inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned npx installer can depend on current package resolution rather than a reviewed release source.

Mitigation: Install from a reviewed tag, commit, or direct clone when possible, and use the unpinned npx path only when that package resolution is trusted.

Risk: Conversation inputs and generated derivatives can contain private transcripts, identifiers, source paths, hashes, or institutional records.

Mitigation: Process only material the user is authorized to analyze, keep original evidence private and unchanged, use --source-label when local paths are sensitive, and review outputs before sharing.

Risk: The validator checks structure, not truth, consent, speaker attribution, redaction completeness, or whether actions were actually authorized.

Mitigation: Compare consequential claims and proposed records against the original source, and require explicit authority before sending follow-ups or writing canonical memory.

## Reference(s):

- [README](README.md)
- [Evidence policy](references/evidence-policy.md)
- [Analytical lenses](references/lenses.md)
- [Output contracts](references/output-contracts.md)
- [Security and privacy](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON, with optional shell commands for local segmentation and structural validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include epistemic labels and source locators when available; local helper scripts can segment long transcripts and validate output structure.]

## Skill Version(s):

1.0.0 (source: server release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
