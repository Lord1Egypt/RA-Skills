## Description:

Helps process, quality, and design engineers design poka-yoke mistake-proofing solutions by clarifying error modes, brainstorming options with E-R-F-D-M principles and classic methods, ranking options by effectiveness, and producing implementation-oriented reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, process engineers, quality engineers, supplier quality engineers, and design engineers use this skill to turn a concrete defect, risk, or process error mode into candidate mistake-proofing designs, selection rationale, validation steps, and standardization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write dated TXT and Markdown reports in the current or selected output directory, which can conflict with existing same-date report files.

Mitigation: Choose an explicit output directory or check for existing report filenames before allowing file output.

Risk: The artifact references a helper script and detailed knowledge file that are not included in the submitted files.

Mitigation: Have the agent generate the report directly from the included skill instructions or fail clearly when missing resources are required.

Risk: Poka-yoke recommendations can be incomplete or physically infeasible without process-specific review.

Mitigation: Require process, equipment, or quality engineering review before implementation and mark missing inputs as pending rather than fabricating details.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-poka-yoke-design)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-poka-yoke-design)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain-text report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates dated poka-yoke design reports and may write local TXT and Markdown files in the selected output directory.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
