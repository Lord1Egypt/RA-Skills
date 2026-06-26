## Description: <br>
Extracts comments from Word documents, maps page numbers, and formats them into standardized review opinions for investment banking QC, legal review, and document audit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomyan-zhang](https://clawhub.ai/user/tomyan-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external reviewers use this skill to extract Word document comments and convert them into standardized review opinions. It is intended for investment banking quality control, legal review, and document audit workflows where page references and concise revision requests matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Microsoft Word automation and requires the pywin32 dependency on a Windows environment. <br>
Mitigation: Install it only where Microsoft Word automation is acceptable and the pywin32 dependency has been approved. <br>
Risk: Extracted comments and nearby document text become visible to the agent during rewriting. <br>
Mitigation: Use trusted documents and avoid processing sensitive content unless the agent environment is approved for that data. <br>
Risk: Physical page numbers may differ from displayed page numbers in documents with cover pages, front matter, or custom numbering. <br>
Mitigation: Review the page number note and apply an offset correction when displayed numbering differs from physical page order. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomyan-zhang/word-comments-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON extraction output followed by a polished Markdown/plain-text review opinion list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows with Microsoft Word and pywin32 for page number retrieval; extracted comments and nearby document text are visible to the agent for rewriting.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
