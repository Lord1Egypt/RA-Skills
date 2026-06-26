## Description: <br>
Refactors AGENTS.md files into a minimal root file plus topic-specific follow-up docs using progressive disclosure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit, propose, or apply refactors to AGENTS.md and CLAUDE.md guidance, splitting monolithic instruction files into a minimal root file plus focused topic documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apply mode can change repository instruction files and alter future agent behavior. <br>
Mitigation: Use review or proposal mode first for sensitive repositories, then apply changes only after reviewing the planned AGENTS.md and topic-document diff. <br>
Risk: Conflicting, stale, or vague instructions may be preserved, moved, or removed incorrectly if the repository guidance is incomplete. <br>
Mitigation: Pause on conflicts, present the exact disagreement to the user, and require a choice before rewriting; call out deletion candidates for review. <br>


## Reference(s): <br>
- [Principles and heuristics](references/principles.md) <br>
- [Project homepage](https://github.com/Fei2-Labs/skill-genie) <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/refactor-agents-md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance, audit findings, proposed file structures, and repository instruction-file edits when apply mode is selected] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can operate in review-only, proposal, or apply-refactor mode depending on user intent.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
