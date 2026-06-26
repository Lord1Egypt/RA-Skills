## Description: <br>
Builds a related-works report from one or more paper Markdown files by extracting Related Works sections, deduplicating cited papers, retrieving arXiv abstracts through Tavily, and assembling a final Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[red0orange](https://clawhub.ai/user/red0orange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, reviewers, and developers use this skill to turn paper Markdown files into an auditable related-works report in a chosen work folder. It is useful when source papers are already available as Markdown and the user needs citation extraction, deduplication, abstract lookup, and final report assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper titles and related lookup data may be sent to Tavily and arxiv.org during abstract retrieval. <br>
Mitigation: Use a dedicated work folder and avoid confidential manuscripts unless those external lookups are acceptable. <br>
Risk: Citation extraction, deduplication, and retrieved abstracts may be incomplete or mismatched. <br>
Mitigation: Review the intermediate artifacts and final report before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/red0orange/related-works-report-from-paper-mds) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with intermediate Markdown and JSONL work artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes all process artifacts under the user-selected work folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
