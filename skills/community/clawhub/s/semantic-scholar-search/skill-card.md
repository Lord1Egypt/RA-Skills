## Description: <br>
Provides a compatibility-layer academic search over the Semantic Scholar API for papers and authors, returning metadata such as citations, abstracts, venues, and source URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to search Semantic Scholar for papers or authors from an agent workflow and inspect concise academic metadata. It is also retained as a backward-compatible entry point for users migrating to the unified search skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Semantic Scholar. <br>
Mitigation: Avoid submitting confidential, personal, or proprietary queries unless that disclosure is acceptable. <br>
Risk: The Python requests dependency may be unavailable in some runtimes. <br>
Mitigation: Confirm requests is installed before using the skill in a target OpenClaw environment. <br>


## Reference(s): <br>
- [Semantic Scholar API](https://api.semanticscholar.org/) <br>
- [Semantic Scholar Graph API endpoint](https://api.semanticscholar.org/graph/v1) <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/semantic-scholar-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Plain text search results with paper or author metadata and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result fields may include titles, authors, years, citation counts, venues, abstracts or TLDRs, and URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
