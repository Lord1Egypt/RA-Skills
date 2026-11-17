## Description:

Surgical quick fix skill for small bugs, typos, simple changes, and clearly targeted edits that can be read, fixed, and verified with minimal tool use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakedoshadow](https://clawhub.ai/user/nakedoshadow)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill for narrowly scoped code fixes where the target file or issue is already clear, followed by a small verification step when local tooling is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification commands can execute local repository code or unsafe shell strings.

Mitigation: Run the skill only in trusted repositories or a sandbox, and use argument-safe command execution for verification.

Risk: TypeScript verification may use unpinned npx tooling and can fetch npm packages despite the artifact claiming no network access.

Mitigation: Prefer pinned local project tooling or disable network access before running npx-based verification.

Risk: Broad quick-fix trigger phrases may apply the skill to tasks that need deeper investigation.

Mitigation: Use it only for small, clearly targeted edits and escalate when the root cause, file scope, or expected fix is unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nakedoshadow/skills/shadows-oneshot-fix)
- [Publisher Homepage](https://clawhub.ai/NakedoShadow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Concise markdown or plain text fix summary with file, change, and verification result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local compile check or targeted test result when available.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
