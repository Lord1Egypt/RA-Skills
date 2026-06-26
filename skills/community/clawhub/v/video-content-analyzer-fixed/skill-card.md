## Description: <br>
Downloads videos from Bilibili, Douyin, YouTube, and similar platforms, then uses AI transcription and analysis to summarize speech, structure, pacing, hooks, and key content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content analysts, marketers, and developers use this skill to turn video URLs into structured content analysis reports with transcripts, key-frame observations, hook analysis, pacing notes, summaries, and optional publishing or storage outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video transcripts, reports, and metadata can be sent to OpenAI and optionally stored in Supabase or published to Feishu. <br>
Mitigation: Use only approved videos and transcripts, apply least-privilege API keys, confirm Supabase RLS and Feishu page visibility, and verify deletion or retention procedures before use. <br>
Risk: The workflow runs download and media-processing commands against user-provided video URLs. <br>
Mitigation: Run in a controlled working directory, review generated commands before execution, avoid system-wide package changes where possible, and confirm rights to analyze the source video. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/video-content-analyzer-fixed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis report with transcript sections, tables, command examples, and optional JSON/API payload guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local downloaded media, extracted audio, key-frame images, Supabase metadata records, and Feishu Wiki reports when the corresponding tools and credentials are configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
