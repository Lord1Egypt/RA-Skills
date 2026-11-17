## Description:

Audit code for "vibe coding sins" - patterns that indicate AI-generated code was accepted without proper review - and produce a scored report card with fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit Python, TypeScript, and JavaScript files, directories, or git diffs for review gaps, code quality issues, and security patterns associated with insufficiently reviewed AI-generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source files can be sent to configured LLM providers during analysis.

Mitigation: Use heuristic mode by running without ANTHROPIC_API_KEY, OPENAI_API_KEY, or openclaw llm for sensitive code, and scope scans to paths that are safe to share.

Risk: Generated findings and fix diffs may be incorrect, incomplete, or unsafe.

Mitigation: Treat reports and patches as untrusted suggestions that require human review before any code changes are applied.

Risk: Reports may directly include untrusted model output.

Mitigation: Review rendered reports before redistributing them and avoid treating report text as executable instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tkuehnl/skills/vibe-check)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with score tables, category breakdowns, findings, optional unified diff patches, and optional README badge Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the report to a user-specified output file; fix suggestions are proposed diffs only and are not applied automatically.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
