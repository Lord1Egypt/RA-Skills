## Description: <br>
Distills public social-video and short-form media into transcripts, summaries, humor reads, best lines, caption ideas, replies, and theme extractions using platform captions or browser AI before local ASR fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little7unifai](https://clawhub.ai/user/little7unifai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to quickly understand public short-form video, recover captions when available, and produce concise summaries, quotes, humor structure, captions, replies, or theme notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts, notes, or recovered dialogue may be sent to Gemini/Google or NotebookLM through browser AI. <br>
Mitigation: Use a dedicated browser profile, avoid private or regulated content without explicit approval, and disclose when external browser AI is used. <br>
Risk: Media and caption files may be written locally during caption extraction or media download workflows. <br>
Mitigation: Use task-specific local directories with appropriate access controls and delete downloaded media or captions after use. <br>
Risk: A distillation may blend directly supported transcript content with inferred context, especially when captions are unavailable or rough notes are used. <br>
Mitigation: Separate direct transcript evidence from inference and state when captions were unavailable or a rough transcript was used. <br>


## Reference(s): <br>
- [Prompt patterns](references/prompts.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise text sections and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May separate directly supported transcript evidence from inferred context and may list local caption or media files produced by helper scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
