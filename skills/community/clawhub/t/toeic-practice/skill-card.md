## Description:

Daily TOEIC practice coach for a user scoring 600+. Delivers one focused session daily for Parts 5, 6, and 7, explains answers with grammar and vocabulary notes, and targets improvement toward 700+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cngvc](https://clawhub.ai/user/cngvc)

### License/Terms of Use:

MIT-0

## Use Case:

TOEIC learners scoring around 600+ use this skill for daily reading-focused homework in Parts 5, 6, and 7, with answer explanations that reinforce grammar, vocabulary, and distractor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a small local state file to track the TOEIC part rotation.

Mitigation: Install and run it only in an agent workspace where this local memory behavior is expected.

Risk: The skill is scoped to English TOEIC reading practice and may not meet needs for listening sections or non-English explanations.

Mitigation: Use it for Parts 5, 6, and 7 practice, and request a different explanation language explicitly if needed.

## Reference(s):

- [Toeic Practice on ClawHub](https://clawhub.ai/cngvc/skills/toeic-practice)
- [Publisher profile](https://clawhub.ai/user/cngvc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style instructional text with original TOEIC practice questions and explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Practice is limited to TOEIC Parts 5, 6, and 7 and uses a small local state file to rotate the daily part.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
