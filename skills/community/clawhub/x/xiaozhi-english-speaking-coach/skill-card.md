## Description:

An English speaking practice coach that guides learners through warmups, role-play, impromptu speaking, pronunciation practice, and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

External English learners, especially school-age students, use this conversational coach for short warmups, role-play, impromptu speaking, pronunciation practice, and review. It supports student-selected English or bilingual practice and carries a profile across sessions only with consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes that student conversation topics may be added to interest profiles without a clear privacy notice identified by the scan.

Mitigation: Before using profiles, confirm students are told what information may be saved; keep profile and cross-skill sharing disabled unless the required consent is present.

Risk: Pronunciation feedback can be inaccurate when the platform provides text or transcription without audio scoring.

Mitigation: Limit feedback to wording, grammar, expression, and fluency unless audio scoring is available; do not infer phoneme errors from transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizhitang/skills/xiaozhi-english-speaking-coach)
- [Topic bank](artifact/references/topic-bank.md)
- [Role-play scripts](artifact/references/roleplay-scripts.md)
- [Pronunciation issues](artifact/references/pronunciation-issues.md)
- [Morning warmup state machine](artifact/references/morning-warmup-statemachine.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Structured data]

**Output Format:** [Conversational practice prompts, feedback, review summaries, and optional profile entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile reads and writes require consent; phoneme-level pronunciation feedback requires audio scoring.]

## Skill Version(s):

2.12.7 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
