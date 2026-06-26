## Description: <br>
Extracts readable markdown from user-provided URLs via a deterministic fallback chain (markdown.new -> r.jina.ai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chdlc](https://clawhub.ai/user/chdlc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to extract readable markdown from specific user-provided URLs for downstream summarization, analysis, or content review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs may be sent to third-party extraction services. <br>
Mitigation: Avoid private intranet links, authenticated pages, signed links, URLs containing tokens or secrets, and links whose existence should remain confidential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chdlc/web-to-md) <br>
- [Publisher profile](https://clawhub.ai/user/chdlc) <br>
- [markdown.new extraction endpoint pattern](https://markdown.new/{URL}?method=ai) <br>
- [r.jina.ai extraction endpoint pattern](https://r.jina.ai/{URL}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and source labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports one provenance label per extracted URL and uses curl when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
