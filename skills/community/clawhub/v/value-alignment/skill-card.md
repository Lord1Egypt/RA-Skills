## Description:

Value Alignment evaluates generated text against helpful, harmless, and honest principles using local heuristic rules, flagging harmful, out-of-bounds, overconfident, or unsupported output before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a local pre-publication gate to score generated content for helpfulness, harmlessness, and honesty before external release or user-facing response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the skill as suspicious because the learner module can write persistent behavioral memory for arbitrary skill directories.

Mitigation: Invoke learner commands only against intended skill directories, review the generated memory file, and avoid storing secrets or sensitive user data in notes or preferences.

Risk: The alignment checker uses heuristic regular expressions and may miss implied, obfuscated, or context-dependent harmful content.

Mitigation: Use the checker as an initial gate, not as a replacement for human review or domain-specific compliance checks for high-risk outputs.

Risk: The honesty score measures cautious wording and does not verify factual correctness.

Mitigation: Pair this skill with factual verification or source review before publishing claims that affect legal, medical, financial, safety, or other high-stakes decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/value-alignment)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object with principle scores, issue list, overall score, and pass/fail status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with the Python standard library; optional learner commands can persist local usage notes and preferences.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
