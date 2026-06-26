## Description: <br>
This skill buffers segmented ASR transcript chunks until an explicit end signal, then rewrites the full segment into fluent written text and optionally translates it when target_language is provided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to post-process completed ASR sessions for meeting notes, interviews, podcasts, video transcript cleanup, or voice dictation workflows where final written quality matters more than real-time captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buffered ASR transcripts can contain sensitive meeting or dictation content. <br>
Mitigation: Confirm host-app retention settings before use and avoid archiving transcript buffers unless retention is explicitly required. <br>
Risk: Final rewriting can accidentally alter names, numbers, or technical terms from noisy ASR input. <br>
Mitigation: Use a domain lexicon where available and review final text before relying on it for decisions or records. <br>


## Reference(s): <br>
- [Interface and Product Integration Guide](references/interface-guide-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text final output, with optional implementation guidance for buffering and end-of-stream handling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits a final result only after an explicit end signal; translates only when target_language is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
