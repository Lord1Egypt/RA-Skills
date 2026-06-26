## Description: <br>
Sum2Slides converts plain text or Markdown summaries into structured, editable PowerPoint presentations with configurable templates and themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, productivity users, and teams use this skill to turn meeting notes, research summaries, project updates, and other text content into presentation drafts. It is useful when an agent needs to generate a PPTX deck from supplied text or Markdown with minimal manual formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process chat history, meeting notes, or other sensitive text into presentation files without clear consent when automatic triggers are enabled. <br>
Mitigation: Keep automatic triggers and auto-save disabled by default, require user confirmation before processing chat or meeting content, and restrict input sources to approved files or messages. <br>
Risk: Generated slides may be copied to shared folders or distributed through Slack or email workflows before the content is reviewed. <br>
Mitigation: Require explicit approval before shared-folder, Slack, or email distribution and review generated PPTX content for confidential or inaccurate material. <br>
Risk: Artifact materials include a hardcoded Feishu owner identifier in release guidance. <br>
Mitigation: Remove or replace hardcoded owner identifiers before deployment and configure ownership through environment-specific settings. <br>


## Reference(s): <br>
- [Sum2Slides ClawHub listing](https://clawhub.ai/wwumit/sum2slides) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [TUTORIAL.md](artifact/TUTORIAL.md) <br>
- [OPENCLAW_USAGE_GUIDE.md](artifact/OPENCLAW_USAGE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, Python API examples, YAML configuration, and generated PPTX presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated presentations may contain summarized user-provided text and should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
