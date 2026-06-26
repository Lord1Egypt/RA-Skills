## Description: <br>
Thoth Standard -- Auto-Documentation Engine. Reads your entire project and generates README, API reference, and usage guide. Saved to .md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to scan a project folder and generate starter documentation from its source files, metadata, and extracted Python symbols. It is intended to produce a README, API reference, and usage guide for the selected project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad project source content to the agent/model context during documentation generation. <br>
Mitigation: Run it only on repositories you are comfortable exposing, review PROJECT_PATH first, and remove secrets or sensitive files before use. <br>
Risk: The install step uses pip in the system Python environment. <br>
Mitigation: Use an isolated Python environment instead of system Python when installing dependencies. <br>
Risk: Generated documentation files may overwrite existing files in the selected output directory. <br>
Mitigation: Choose an OUTPUT_DIR where README.md, API_REFERENCE.md, and USAGE_GUIDE.md can be safely written, then review the generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/thoth) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown documents saved as README.md, API_REFERENCE.md, and USAGE_GUIDE.md, with inline shell and Python snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LICENSE_KEY and PROJECT_PATH; OUTPUT_DIR controls where generated documentation is written.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
