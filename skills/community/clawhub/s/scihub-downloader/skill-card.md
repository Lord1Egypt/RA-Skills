## Description: <br>
Downloads academic papers from open-access sources and, when allowed by the user, Sci-Hub mirrors with direct PDF link extraction. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Doradx](https://clawhub.ai/user/Doradx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and research-support agents use this skill to locate and download papers by DOI, PMID, arXiv ID, URL, or title. It prefers open-access services and provides an open-access-only option when Sci-Hub fallback is not appropriate. <br>

### Deployment Geography for Use: <br>
Global, subject to local copyright and access laws. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact Sci-Hub mirrors and retrieve PDFs from unofficial sources when open-access sources fail. <br>
Mitigation: Use --oa-only when only legal open-access sources are acceptable, and confirm that any mirror use complies with local law and institutional policy. <br>
Risk: Downloaded PDFs from unofficial mirrors may be untrusted files. <br>
Mitigation: Treat downloaded PDFs as untrusted content, scan them before opening, and avoid submitting sensitive unpublished research queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Doradx/scihub-downloader) <br>
- [DOI Format Reference](references/doi-formats.md) <br>
- [Sci-Hub Mirrors Reference](references/mirrors.md) <br>
- [Usage Examples for Paper Downloader](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; runtime output is terminal text, optional JSON metadata, and downloaded PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports custom output paths, custom filenames, availability checks, verbose logging, retries, mirror selection, and --oa-only mode.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence and artifact metadata; script VERSION reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
