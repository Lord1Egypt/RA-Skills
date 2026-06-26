## Description: <br>
Research a topic via web search, auto-match a relevant GIF, and log structured notes to Bear using a configurable template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and note-taking users can use this skill to turn a research topic into a structured Bear note with source links, extracted findings, action items, and a matched GIF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and retrieved content may be sent to configured web search, fetch, and GIF services. <br>
Mitigation: Avoid sensitive or proprietary topics unless the configured services are approved for that data. <br>
Risk: Generated notes may include untrusted, inaccurate, or low-quality web content. <br>
Mitigation: Review the generated summary, findings, links, and action items before relying on or sharing the note. <br>
Risk: The skill writes persistent notes to Bear or to a local Markdown fallback file. <br>
Mitigation: Check the destination note or fallback file before storing confidential information or syncing it elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/research-logger-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown research note with shell status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Bear note through grizzly, or falls back to a Markdown file when Bear is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
