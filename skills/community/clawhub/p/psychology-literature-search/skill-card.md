## Description: <br>
This skill helps agents search Chinese and English psychology literature through free academic APIs, format citations, and export results for research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhan599](https://clawhub.ai/user/zhan599) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and research assistants use this skill to find psychology papers, compare metadata from Semantic Scholar, OpenAlex, and CrossRef, and create citation or export files for literature review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external academic APIs, and an optional email address may be shared with OpenAlex or CrossRef as a polite-pool contact. <br>
Mitigation: Use non-sensitive search terms and omit the email address when privacy requirements call for it. <br>
Risk: Export functions write CSV or text citation files to the local path chosen by the user. <br>
Mitigation: Review output filenames and directories before running exports in shared or production workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhan599/psychology-literature-search) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1) <br>
- [OpenAlex Works API](https://api.openalex.org/works) <br>
- [CrossRef Works API](https://api.crossref.org/works) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python examples, returned literature records, CSV exports, and plain-text citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to public academic APIs; optional email can be used as a contact for OpenAlex and CrossRef requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
