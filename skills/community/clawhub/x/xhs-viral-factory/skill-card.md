## Description: <br>
小红书爆款图文全自动生产工厂。支持从 PDF、Markdown 或文件夹提取内容，自动匹配治愈、干货、反直觉、视觉流 4 大模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[less1001](https://clawhub.ai/user/less1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and agent users use this skill to turn local notes, documents, or folders into draft Xiaohongshu posts with titles, body copy, image prompts, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local source files and any optional history file are sent to the configured LLM provider for content generation. <br>
Mitigation: Avoid sensitive private documents, verify the provider endpoint and API key scope, and review generated drafts before publishing. <br>
Risk: The documentation describes PDF input, but security guidance says native PDF extraction is not implemented. <br>
Mitigation: Convert PDFs to text or Markdown before using them as source material. <br>


## Reference(s): <br>
- [XHS Viral Factory Detailed Workflow](references/workflow.md) <br>
- [XHS Viral Factory Patterns](references/prompt_patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/less1001/xhs-viral-factory) <br>
- [Publisher Profile](https://clawhub.ai/user/less1001) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text draft file with title, body, image prompts, and tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LLM_API_KEY and can optionally use LLM_BASE_URL, LLM_MODEL, and a history file.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
