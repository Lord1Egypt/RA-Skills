## Description: <br>
Extract Xiaohongshu (小红书) posts into Obsidian Markdown notes, with support for single posts, batch extraction, and optional video transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmin1113](https://clawhub.ai/user/jmin1113) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal knowledge-management users use this skill to convert Xiaohongshu or RedNote links into Obsidian-ready Markdown notes with post metadata, images, and optional video transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Xiaohongshu login cookies that could expose an account session. <br>
Mitigation: Use only a low-risk Xiaohongshu account, treat ~/.openclaw/xhs-cookies.json like a password, and delete or rotate the cookie file after use. <br>
Risk: Running the extractor on untrusted links can increase account and transport risk. <br>
Mitigation: Avoid untrusted links unless the extractor is patched to enforce the Xiaohongshu hostname and keep normal HTTPS certificate verification enabled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jmin1113/xhs-to-obsidian) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, JSON status output, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves notes to an Obsidian vault path and may append video transcription text when optional dependencies are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
