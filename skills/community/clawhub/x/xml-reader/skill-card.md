## Description: <br>
Read and parse XML from construction systems - P6 schedules, BSDD exports, IFC-XML, COBie-XML. Convert to pandas DataFrames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, construction data analysts, and project controls teams use this skill to parse XML exports from construction systems and turn elements from P6, IFC-XML, COBie-XML, and BSDD sources into structured pandas DataFrames for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local construction data files supplied by the user. <br>
Mitigation: Install and use it only when local file access is intended, and provide only trusted project files. <br>
Risk: Untrusted or unusually large XML inputs can create ordinary parsing reliability and resource-use risk. <br>
Mitigation: Keep XML inputs trusted and reasonably sized, validate inputs before parsing, and report parsing errors clearly. <br>
Risk: Documentation mentions CSV, Excel, and JSON handling beyond the primary XML parsing scope. <br>
Mitigation: Verify non-XML export or conversion behavior before relying on it in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/xml-reader) <br>
- [Publisher homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Python code examples and structured tables when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest Excel, CSV, or JSON export options when relevant.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
