## Description: <br>
个人日记自动化 skill。用于按天生成日记文本并导出 1080px 图片；支持首次自动初始化、读取 SOUL/MEMORY/每日记忆素材、保持写作风格连续性。适用于用户要求“写日记/生成日记图片/补昨天日记/自动日记归档”等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1204TMax](https://clawhub.ai/user/1204TMax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to generate dated diary entries from configured personal memory sources and export a 1080px-wide diary image for archiving, sharing, or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads configured personal memory files and diary history, which can contain private information. <br>
Mitigation: Review config.yaml before first use and keep SOUL, MEMORY, daily memory, diary output, and optional news-summary paths limited to intended local files. <br>
Risk: The skill writes diary text and rendered images to local output paths. <br>
Mitigation: Confirm the diary output directory before running and avoid sharing generated diary images without reviewing their contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1204TMax/riji) <br>
- [README](artifact/README.md) <br>
- [Initialization Workflow](artifact/INIT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Diary text in Markdown plus a rendered PNG image file and returned output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured local paths and a 1080px default image width.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
