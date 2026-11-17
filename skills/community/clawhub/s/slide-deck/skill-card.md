## Description:

Generate beautiful HTML slide presentations from markdown or plain text as a single browser-openable HTML file with a dark theme, smooth animations, and speaker notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to turn a topic, outline, markdown, or text into a ready-to-present HTML slide deck.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated slide decks may load third-party CDN code from jsDelivr.

Mitigation: Review generated HTML and confirm the CDN dependency is acceptable before presenting or sharing the deck.

Risk: Untrusted markdown or text could be converted into unsafe or misleading HTML content.

Mitigation: Avoid attacker-supplied content unless the agent escapes or sanitizes it, and inspect generated HTML before sharing it externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vanthienha199/skills/slide-deck)
- [Reveal.js CDN stylesheet](https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.min.css)
- [Reveal.js CDN script](https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.min.js)
- [Reveal.js Highlight Plugin CDN script](https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code]

**Output Format:** [A single HTML file containing reveal.js slides.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks load reveal.js assets from jsDelivr and are intended to be reviewed before external sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
