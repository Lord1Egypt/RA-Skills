## Description: <br>
Fetches WeChat public account articles and converts them into offline Markdown, HTML, plain text, JSON, or Excel files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luojiangyong](https://clawhub.ai/user/luojiangyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive or reformat WeChat article links into local files for reading, sharing, analysis, or batch processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes web requests to WeChat and saves converted article files locally, which can create many files during batch or HTML export. <br>
Mitigation: Review the requested article links and output location before running batch or HTML exports. <br>
Risk: The Python scripts rely on undeclared runtime dependencies for parsing, Markdown conversion, and Excel output. <br>
Mitigation: Run the skill in a trusted Python environment and install only the dependencies needed for the selected export formats. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with local file outputs in Markdown, HTML, text, JSON, or Excel formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save article files and localized HTML assets to the user's Desktop or a provided output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
