## Description: <br>
Transcribes video or audio with Whisper, refines the transcript, and drafts platform-specific Chinese content for Zhihu, WeChat, and Xiaohongshu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artminding](https://clawhub.ai/user/artminding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and knowledge workers use this skill to turn Chinese video or audio into timestamped transcripts, edited Markdown, and channel-ready social publishing drafts. It is also useful for agents that need a repeatable transcription-to-content workflow with user review points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, regulated, legal, medical, business, or unpublished recordings may be exposed through transcript handling or downstream content drafting. <br>
Mitigation: Use only recordings appropriate for the agent environment, confirm the output directory before processing, and review generated transcript and draft files before sharing. <br>
Risk: The skill may use web_search or web_fetch to supplement transcript terms, which can send transcript-derived topics to online services. <br>
Mitigation: For sensitive recordings, instruct the agent to avoid web_search and web_fetch, then manually provide any required terminology or background context. <br>
Risk: User preferences may be reused from MEMORY.md in later runs. <br>
Mitigation: Inspect or clear MEMORY.md when preferences should not persist across transcription and drafting tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/artminding/video-transcript-pro) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [Whisper open-source project](https://github.com/openai/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [TXT and Markdown files with timestamped transcript text, edited drafts, platform-specific publishing copy, correction review tables, and optional image prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local output files next to the source media or in a transcript output directory; content should be reviewed before publication.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence; artifact SKILL.md lists v2.3 and package.json lists 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
