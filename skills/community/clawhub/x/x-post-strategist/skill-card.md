## Description:

Turns ideas, notes, articles, reports, and technical material into X posts or threads with tone matching, account-aware length handling, fact checks, and optional image recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, founders, developers, researchers, and operators use this skill to turn rough ideas or source material into publishable X posts and threads that fit the chosen account type, format, audience, tone, and factual-risk constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional renderer opens local HTML in Chrome without blocking scripts or network access.

Mitigation: Render only trusted, self-contained HTML; avoid untrusted copied markup; and consider blocking network or JavaScript and updating dependencies before rendering cards.

Risk: Optional draft saving can write generated content to a local notes vault path.

Mitigation: Enable saving only with explicit user consent and review the resolved OBSIDIAN_VAULT_PATH or chosen folder before the first write.

Risk: Drafts may cover real-time, financial, legal, medical, political, scientific, or otherwise high-stakes claims.

Mitigation: Verify claims with available tools, mark uncertainty clearly, and avoid presenting unverified claims as fact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/x-post-strategist)
- [README](artifact/README.md)
- [Chinese AI / Tech X post reference](artifact/chinese-ai-tech-posts.md)
- [Render image setup](artifact/render-image-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text drafts with optional image briefs, HTML/CSS snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include character-count checks, self-review scores, optional local markdown saves, and optional PNG rendering guidance for text/data graphics.]

## Skill Version(s):

0.14.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
