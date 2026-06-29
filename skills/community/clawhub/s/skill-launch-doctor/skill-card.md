## Description: <br>
Audit, score, and improve AgentSkills-style skill folders for trigger quality, progressive disclosure, resource references, cross-agent compatibility, safety risks, install friction, marketplace positioning, and launch readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to audit AgentSkill-style skill folders before publishing, sharing, installing, or rolling them out. It helps agents produce launch readiness reports with scores, prioritized findings, description rewrites, compatibility notes, remaining risks, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence notes powerful maintainer workflows that can affect live services or public content when run with authenticated credentials. <br>
Mitigation: Use authenticated moderation, email, PR-commenting, proof publishing, production migration, or similar workflows only when the user explicitly requests them and the workflow provides confirmation, dry-run, or signoff gates. <br>
Risk: Launch-readiness guidance and proposed rewrites may introduce inaccurate or misleading skill behavior claims if applied without review. <br>
Mitigation: Review generated findings and rewrites against the source skill before publishing, and keep capability, compatibility, safety, pricing, license, and owner claims grounded in the artifact evidence. <br>


## Reference(s): <br>
- [Description Patterns](references/description-patterns.md) <br>
- [Skill Launch Rubric](references/launch-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, with optional JSON output from the bundled audit script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include an overall score and verdict, P0/P1 findings with concrete fixes, optional description rewrite, compatibility notes, remaining launch risks, and the smallest next action.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
