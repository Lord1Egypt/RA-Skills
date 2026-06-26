## Description: <br>
WOSO Lib is a Chinese-language conversational knowledge base for women’s football, covering player and coach stories, football history, tactics, sport psychology, workload, physiology, and industry reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wongeven](https://clawhub.ai/user/wongeven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, writers, researchers, coaches, athletes, media workers, and football fans use this skill to ask conversational questions about women’s football history, biographies, coaching, tactics, sport science, workload, physiology, and industry context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms may activate the skill for general World Cup, workload, or menstrual-cycle questions. <br>
Mitigation: Review routing behavior before installation and prefer explicit women’s-football context when invoking the skill. <br>
Risk: Some biography notes include self-harm, suicide-crisis, and substance-misuse material without a warning. <br>
Mitigation: Add user-facing content warnings or review sensitive biography responses before broad deployment. <br>
Risk: Knowledge-base summaries may be mistaken for complete primary sources. <br>
Mitigation: Use the skill for orientation and cite or consult original books, reports, or official documents for high-stakes research. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wongeven/woso-lib) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [WOSO reports outline](artifact/references/woso_reports_outline.md) <br>
- [AFC WCL 2024/25 technical report outline](artifact/references/afc_wcl_2025_technical_report_outline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text conversational answers in Chinese, with source titles named when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only knowledge responses; no command execution or external system access is described by the security evidence.] <br>

## Skill Version(s): <br>
2.12.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
