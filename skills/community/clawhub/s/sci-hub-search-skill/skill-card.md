## Description: <br>
AI-powered tool for searching and downloading academic papers through Sci-Hub. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External researchers and developers use this skill to search for academic papers by DOI, title, or keyword, retrieve metadata, and download available PDFs through Sci-Hub-backed command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download content from broad URLs and write files to local paths. <br>
Mitigation: Run it in an isolated Python environment, download only trusted Sci-Hub or PDF URLs, and choose a non-sensitive output directory. <br>
Risk: Dependency and installer behavior may change outside the reviewed artifact. <br>
Mitigation: Review and pin Python dependencies before use, and avoid curl-piped installers where possible. <br>
Risk: Sci-Hub access and downloaded-paper use may be restricted by local rules or copyright obligations. <br>
Mitigation: Use the skill only where its Sci-Hub access pattern is allowed and follow the artifact guidance to respect copyright and local law. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/JackKuo666/sci-hub-search-skill) <br>
- [Crossref Works API](https://api.crossref.org/works) <br>
- [scihub Python Package](https://pypi.org/project/scihub/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON, Markdown guidance with bash code blocks, and downloaded PDF files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write search results or metadata to a user-specified output file and can save downloaded PDFs to a user-specified path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
