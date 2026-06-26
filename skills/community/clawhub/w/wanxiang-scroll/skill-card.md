## Description: <br>
Wanxiang Scroll is a Chinese creative-writing and interactive-story skill pack for switching among 56 prose styles, collaborative storytelling, turn-based life simulation, fiction planning, style polishing, and reusable prompt references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandanllab](https://clawhub.ai/user/dandanllab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, roleplay users, and agent developers use this skill as a Chinese-language fiction toolkit for guided story generation, interactive narrative play, life-simulation sessions, prose style selection, editing, and prompt-template reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crawler helper scripts contact third-party novel APIs and write downloaded text files. <br>
Mitigation: Review the selected crawler command, destination path, and applicable rights or terms before execution. <br>
Risk: The novel text cleaner overwrites the source file when no separate output path is provided. <br>
Mitigation: Run it on a copy or provide an explicit output file when preserving the original text matters. <br>
Risk: Immersive roleplay and persistent style instructions may conflict with user, platform, or safety requirements. <br>
Mitigation: Treat the artifact files as creative references and keep higher-priority instructions and safety policy authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandanllab/wanxiang-scroll) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Reference index](artifact/references/index.md) <br>
- [Core system index](artifact/references/ch01-核心系统/index.md) <br>
- [Interactive story index](artifact/references/ch02-互动故事/index.md) <br>
- [Life simulation index](artifact/references/ch04-人生模拟/index.md) <br>
- [Style system index](artifact/references/ch05-文风系统/index.md) <br>
- [Creation engine index](artifact/references/ch06-创作引擎/index.md) <br>
- [Quality control index](artifact/references/ch07-质量控制/index.md) <br>
- [Online fiction workflow index](artifact/references/ch08-网文创作/index.md) <br>
- [Book analysis and fusion index](artifact/references/ch09-拆书融合/index.md) <br>
- [Novel text cleaner](artifact/references/novel-text-cleaner.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with reusable prompt text, reference files, JSON save templates, Python helper scripts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Chinese-language creative-writing output; includes optional local scripts for text cleaning, analysis, export, and novel crawling.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
