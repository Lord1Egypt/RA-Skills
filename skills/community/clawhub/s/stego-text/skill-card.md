## Description:

Stego Text helps agents encode, decode, and analyze hidden messages in natural-looking prose using textual steganography methods such as probability anomalies, word-count mapping, acrostics, and multi-channel confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to create, decode, or inspect hidden messages embedded in ordinary prose. Appropriate benign uses include puzzles, watermarking research, and defensive analysis of suspected textual steganography.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help create hard-to-detect concealed messages.

Mitigation: Use it only for benign puzzles, watermarking research, or defensive analysis; do not use it to bypass moderation, hide instructions, or conceal sensitive data movement.

Risk: Probabilistic anomaly-based encodings can decode inconsistently across models or readers.

Mitigation: Verify every encoded passage by decoding it before use, and prefer deterministic word-count or acrostic methods when exact recovery matters.

## Reference(s):

- [Encoding Methods - Full Specification](references/encoding-methods.md)
- [Resonance Encoding - Deep Dive](references/resonance-deep-dive.md)
- [ClawHub Skill Page](https://clawhub.ai/morpheis/skills/stego-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language text or Markdown with encoded passages, decoding steps, and analysis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include hidden-message carrier text, decoded message text, method selection guidance, and verification notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
