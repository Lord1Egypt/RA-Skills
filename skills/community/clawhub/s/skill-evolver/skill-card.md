## Description: <br>
A complete skill lifecycle manager for discovering, orchestrating, fusing, and evolving skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testlbin](https://clawhub.ai/user/testlbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide whether to solve a task natively, orchestrate existing skills, fuse partial-fit skills, or preserve a validated workflow as a reusable skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill-management workflows can change which skills an agent installs, audits, combines, or reuses. <br>
Mitigation: Approve installs, audits, and new skill creation deliberately; review registry skills and inspect generated fused skills before reuse. <br>
Risk: Some workflows may propose npm, pnpm, npx, or removal commands. <br>
Mitigation: Verify package sources, selected skill slugs, and exact target paths before running commands; run removal commands only when the path is the intended skill directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/testlbin/skill-evolver) <br>
- [Skill Search Workflow](references/skill-search.md) <br>
- [Skill Inspector Workflow](references/skill-inspector.md) <br>
- [Skill Fusion Workflow](references/skill-fusion.md) <br>
- [Vercel Skills CLI](https://github.com/vercel-labs/skills) <br>
- [ClawHub CLI Documentation](https://docs.openclaw.ai/zh-CN/tools/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown reports, plans, checkpoints, command snippets, and optional generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces phase artifacts such as intent analysis, candidate lists, inspection reports, orchestration plans, fusion specifications, verification reports, and audit reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
