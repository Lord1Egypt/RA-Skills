## Description:

Reviewcourt helps agents turn completed Tencent Meeting requirement, PRD, or technical review meetings into evidence-backed review recommendations, including Pass, Conditional Pass, Reject, or Insufficient Info outcomes, blockers, quote citations, acceptance criteria drafts, and PRD discrepancy checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, engineering leads, QA reviewers, and delivery teams use this skill after a completed Tencent Meeting review to decide whether requirements can proceed, what blockers remain, and whether a PRD reflects the meeting outcome. It is intended for evidence-based review recommendations, not general meeting minutes, live meeting monitoring, automatic document changes, or people performance evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive meeting recordings, transcripts, participant data, and related PRDs through a local Tencent Meeting CLI.

Mitigation: Install and authorize the CLI only in a trusted, isolated workspace, avoid unrelated sensitive files, and keep transcript and PRD access limited to the review task.

Risk: The release asks users to install a mutable global CLI package before processing meeting evidence.

Mitigation: Prefer a pinned or isolated tmeet installation, verify the package source before OAuth authorization, and review proposed commands before execution.

Risk: Generated review recommendations can be incorrect or misleading if based on smart minutes alone or incomplete transcript permissions.

Mitigation: Require paragraph-level transcript evidence for verdicts, stop for user confirmation when permissions are missing, and label unsupported conclusions as information insufficient.

## Reference(s):

- [Review playbook](references/review-playbook.md)
- [ClawHub skill page](https://clawhub.ai/chris1wang3/skills/reviewcourt)
- [Project homepage](https://github.com/Chris1Wang3/HammerRoom-Skills/tree/master/reviewcourt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with evidence labels, tables, and inline shell commands when Tencent Meeting data must be retrieved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs review recommendations with traceable evidence IDs, blockers, pending confirmations, acceptance criteria drafts, and optional PRD discrepancy matrices.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
