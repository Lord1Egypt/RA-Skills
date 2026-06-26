## Description: <br>
Extracts clean page text from URLs through the AISA Tavily extraction API for summarization, comparison, and evidence review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they already have URLs and need clean extracted page text for summarization, comparison, or evidence review. It is most appropriate as a web-content intake step before downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled client exposes broader search and AI synthesis commands beyond URL extraction. <br>
Mitigation: Invoke only the extract subcommand for URL body extraction unless the broader commands are intentionally reviewed and approved. <br>
Risk: AISA_API_KEY is required, and URLs, queries, and retrieved content may be sent to AISA endpoints. <br>
Mitigation: Use an appropriate key and avoid private or sensitive URLs unless AISA's handling of that data is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/tavily-extract-zh) <br>
- [AISA service](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from the Python CLI, with extracted page content printed to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends URLs, queries, and retrieved content to AISA endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
