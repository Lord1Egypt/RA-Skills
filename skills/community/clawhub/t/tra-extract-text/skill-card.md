## Description: <br>
Extract text content from web pages using trafilatura CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-processing agents use this skill to extract readable text, Markdown, HTML, JSON, or XML from web pages and optionally save extracted content to a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-specified URLs, which can expose private-network or sensitive pages if targets are not chosen deliberately. <br>
Mitigation: Use only URLs that are authorized for extraction and avoid localhost, private-network, or sensitive pages unless access is intentional. <br>
Risk: The skill can write extracted content to files, which can overwrite or place content in unintended paths. <br>
Mitigation: Review output paths before saving extracted content. <br>
Risk: The skill depends on the external trafilatura CLI package. <br>
Mitigation: Install trafilatura from a trusted Python package source, preferably in a virtual environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/tra-extract-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and extracted content examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include metadata fields such as title, author, and date when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
