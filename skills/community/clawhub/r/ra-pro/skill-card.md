## Description: <br>
Ra Pro -- Deep Research Intelligence. 12+ sources, multi-angle analysis, competitive breakdowns, executive brief + detailed report, .md and .docx export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Ra Pro to research a user-provided topic and produce an executive-style intelligence report with multiple viewpoints, competitive context when requested, and formatted citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a Python package during setup. <br>
Mitigation: Use a virtual environment or otherwise review the impact of the pip install command before running it. <br>
Risk: The skill saves generated research reports locally and can use a user-provided output path. <br>
Mitigation: Set OUTPUT_FILE only to a filename or trusted path, check for existing files before running, and avoid sensitive research topics unless local storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/ra-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with cited references, plus setup snippets and local file output guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses RESEARCH_TOPIC and LICENSE_KEY, supports optional depth, angle, competitive-analysis, citation-style, and output-file settings, and saves a local Markdown report.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
