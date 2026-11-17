## Description:

Manual browser-driven X surfing workflow that scrolls the For You feed, opens post details, translates or summarizes posts into Chinese, deduplicates by status URL, and appends structured notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaima2022](https://clawhub.ai/user/kaima2022)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manually monitor X For You content through an attached Chrome session and turn selected posts into Chinese Markdown notes. It is suited to tracking AI, tools, and product updates when the user explicitly wants browser-based review rather than API scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses an authenticated live Chrome session, so collected content may reflect private or account-specific timeline context.

Mitigation: Use a dedicated Chrome profile or isolated X tab and confirm the browser relay is attached only where intended before running.

Risk: The artifact defines a hard-coded local Markdown output path, which could write collected timeline content into an unexpected project file.

Mitigation: Confirm or change the output file path before execution.

Risk: Timeline posts may contain second-hand or unverified claims.

Mitigation: Use the skill's value, verification, and noise comment labels, and verify important claims against the original linked post before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaima2022/skills/x-manual-surf-notes)
- [Browser scrape snippets](artifact/references/browser-scrape-snippets.md)
- [ClawHub listing text](artifact/references/listing.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown notes with structured batch entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends batches with time, content, link, and comment fields; deduplicates entries by normalized X status URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
