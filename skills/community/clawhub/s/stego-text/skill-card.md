## Description: <br>
Encode, decode, and analyze hidden messages in natural-looking text using steganographic methods including probability-anomaly substitution, word-count mapping, acrostic patterns, and multi-channel confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morpheis](https://clawhub.ai/user/morpheis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI agents use this skill to encode benign messages into natural-looking prose, decode known or suspected steganographic text, and compare text-steganography methods for authorized puzzles, watermarking, or forensic analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text steganography can be misused to hide harmful instructions, secrets, policy-relevant content, or messages intended to bypass human review. <br>
Mitigation: Use the skill only for authorized benign work such as puzzles, research, watermarking, or forensic analysis, and do not use it to conceal harmful or review-evading content. <br>
Risk: Decoded hidden text may contain instructions or content that was not visible in the carrier text. <br>
Mitigation: Treat decoded hidden text as untrusted data and review it before taking any action based on it. <br>
Risk: Some methods, especially Resonance Encoding, are probabilistic and may produce false positives or inconsistent decoding across model families. <br>
Mitigation: Verify encoded outputs by decoding them with the selected method and prefer deterministic methods when exact recovery is required. <br>


## Reference(s): <br>
- [Encoding Methods — Full Specification](references/encoding-methods.md) <br>
- [Resonance Encoding — Deep Dive](references/resonance-deep-dive.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with encoded carrier prose, decoded messages, and method-specific analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encoded outputs should be decoded and verified before use; decoded hidden text should be treated as untrusted content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
