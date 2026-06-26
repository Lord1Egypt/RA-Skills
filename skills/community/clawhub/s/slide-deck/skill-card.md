## Description: <br>
Generate HTML slide presentations from markdown or plain text with a dark reveal.js theme, keyboard navigation, animations, and optional speaker notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business users can use this skill to turn a topic, outline, text, or markdown into a browser-ready HTML presentation. It is suited for pitch decks, technical presentations, and structured slide drafts that need quick visual formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks may include speaker notes or user-provided material that is not intended for public sharing. <br>
Mitigation: Review the generated HTML before presenting or distributing it, especially any speaker notes. <br>
Risk: A generated slide deck can overwrite an existing file if the requested output path or generated filename collides with important work. <br>
Mitigation: Choose a descriptive output path and check before replacing existing presentation files. <br>
Risk: Opened decks fetch reveal.js assets from jsDelivr by default. <br>
Mitigation: Replace CDN links with local copies when offline use, stricter supply-chain controls, or network isolation are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vanthienha199/slide-deck) <br>
- [Publisher profile](https://clawhub.ai/user/vanthienha199) <br>
- [reveal.js browser presentation framework](https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.min.js) <br>
- [reveal.js default stylesheet](https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.min.css) <br>
- [reveal.js syntax highlighting plugin](https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files] <br>
**Output Format:** [Single HTML file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses reveal.js assets from jsDelivr unless replaced with local copies; dark theme, responsive layout, keyboard navigation, optional speaker notes, and code highlighting are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
