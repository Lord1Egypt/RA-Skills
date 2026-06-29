## Description: <br>
工具软件教程自动生成器会根据任意工具或软件名称，聚合中文互联网教程资源并生成结构完整的交互式 HTML 教程报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, learners, and technical writers use this skill to research a named tool or software product across Chinese-language web sources and turn the findings into a structured tutorial report. It is suited for creating overview, installation, basic usage, advanced tips, FAQ, learning path, and resource sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic tutorial requests may activate the skill unexpectedly. <br>
Mitigation: Review the requested tool or software name before allowing the workflow to search and generate the report. <br>
Risk: The skill writes an HTML report to the workspace root using the tool name in the filename. <br>
Mitigation: Check the generated filename before reusing the same tool name or sharing the workspace output. <br>
Risk: Tutorial content depends on current web search results and may include outdated or low-quality sources. <br>
Mitigation: Review cited resources and validate installation commands, examples, and links before relying on the report. <br>


## Reference(s): <br>
- [Search Guide](artifact/references/search_guide.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/bettermen/tool-tutorial-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance, files] <br>
**Output Format:** [Single-file HTML report with concise Markdown delivery summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated report is saved in the workspace root using the requested tool name in the filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
