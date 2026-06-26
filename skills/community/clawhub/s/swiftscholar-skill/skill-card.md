## Description: <br>
Integrates the SwiftScholar HTTP API for searching, submitting, and analyzing academic papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tokisakix](https://clawhub.ai/user/Tokisakix) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and research-focused agent users use this skill to search literature, submit paper URLs or PDFs for parsing, retrieve paper analyses, manage SwiftScholar favorites, and inspect account usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using SwiftScholar account features requires an API key that could expose account access if shared in chat or logs. <br>
Mitigation: Keep the SwiftScholar API key in the HTTP execution environment only and do not reveal it in natural-language responses. <br>
Risk: Submitting PDFs or URLs may send confidential, unpublished, licensed, or sensitive documents to SwiftScholar. <br>
Mitigation: Confirm before uploads or forced re-parses and avoid submitting documents unless the user is comfortable sending them to SwiftScholar. <br>


## Reference(s): <br>
- [SwiftScholar](https://www.swiftscholar.net) <br>
- [ClawHub release page](https://clawhub.ai/Tokisakix/swiftscholar-skill) <br>
- [Publisher profile](https://clawhub.ai/user/Tokisakix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries and structured JSON-oriented API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SwiftScholar paper IDs, endpoint names, request parameters, guarded PDF links, and quota or usage summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
