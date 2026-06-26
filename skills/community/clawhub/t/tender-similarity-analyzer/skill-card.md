## Description: <br>
Analyzes multiple local tender documents for paragraph-level similarity and produces an HTML duplicate-content report with statistics, status labels, and rewrite suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliwenjing](https://clawhub.ai/user/wuliwenjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Proposal and tender teams use this skill to compare two or more local DOCX, PDF, TXT, or Markdown files and identify repeated or highly similar paragraphs before submission. It is useful when reviewers need an HTML report that highlights duplicate paragraph pairs, aggregate similarity statistics, and suggested rewrite directions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads tender documents and writes an HTML report containing matching paragraph text. <br>
Mitigation: Run it only on documents intended for local review, store the generated report in an approved location, and treat the report as sensitive tender material. <br>
Risk: The release evidence says its zero-outbound and sandbox claims should not be treated as a hard security boundary. <br>
Mitigation: Use normal environment controls for confidential documents and do not rely on the skill's network-isolation claims as the sole protection. <br>
Risk: Dependency installation and document-editing helper paths can change the local environment or files if explicitly invoked. <br>
Mitigation: Install dependencies manually from a reviewed requirements file and avoid helper paths that edit documents unless those changes are intended and backed up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuliwenjing/tender-similarity-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [HTML report file plus console summary and human-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads selected local tender files, writes a local report and audit metadata, and may provide rewrite suggestions without modifying source files during normal analysis.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
