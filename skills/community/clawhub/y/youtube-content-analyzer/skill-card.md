## Description: <br>
Analyzes YouTube subtitles or transcript files to produce concise summaries, key points, topic tags, notable quotes, and basic content statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, analysts, and other agents use this skill to turn YouTube subtitles, SRT/VTT/TXT files, or folders of transcripts into structured analysis reports for quick content review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated local reports may contain private or sensitive video transcript content. <br>
Mitigation: Avoid providing sensitive transcripts unless local persistence is acceptable, and delete generated reports when they are no longer needed. <br>
Risk: Manual installation commands may fetch mutable files from a branch rather than an immutable release. <br>
Mitigation: Review the downloaded SKILL.md and analyze_content.py before use, and prefer a pinned commit or verified release when installing. <br>


## Reference(s): <br>
- [Analysis Prompt Guide](references/analysis-prompt.md) <br>
- [ClawHub skill page](https://clawhub.ai/mcbaivn/youtube-content-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text report with Markdown-style sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local analysis files under Youtube_Analysis and may include transcript excerpts truncated to 12000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
