## Description: <br>
Combine web and academic search into one smart AISA search mode for balanced research across public web coverage and academic sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and other external users can use this skill when they need one research pass that combines public web results with academic search depth. It is intended for research queries, not credential access or unrelated local data collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled client can send search queries, pasted URLs, extracted URL content, and AISA_API_KEY-authenticated requests to AISA. <br>
Mitigation: Use the skill only when the user intends to share that query or URL with AISA, and avoid private, signed, intranet, localhost, or sensitive document URLs. <br>
Risk: The security verdict is suspicious because the client can do more and send more data than the short skill description clearly explains. <br>
Mitigation: Review the requested mode before running it, especially extract and multi-source modes, and keep usage limited to research-oriented queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/smart-search-aisa) <br>
- [AISA service](https://aisa.one) <br>
- [AISA API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text with search results, citations, summaries, and optional command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; search queries, URLs, and extracted URL content may be sent to AISA.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
