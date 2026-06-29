## Description: <br>
Audits a skill or repository, scopes the build, finds gaps, and emits a machine-readable handoff spec for the next implementation stage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to evaluate Claude Code skills before implementation, identify readiness gaps, and produce a schema-validated handoff spec for a downstream builder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes audit handoff files beside the target repository, which could be committed unintentionally. <br>
Mitigation: Review generated .skill-guidance outputs before commit and redirect or exclude them when audit artifacts should remain local. <br>
Risk: Comparable-skill research may fetch public reference material into temporary storage. <br>
Mitigation: Review local KB and fetch-tool behavior before use in restricted environments, and treat temporary reference caches as disposable. <br>
Risk: Incorrect scoring or handoff guidance could misdirect a downstream skill build. <br>
Mitigation: Review the scorecard, assumptions, and handoff spec before implementation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincentjiang06/skills/skill-guidance) <br>
- [Publisher Profile](https://clawhub.ai/user/vincentjiang06) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.en.md](artifact/README.en.md) <br>
- [Handoff Spec Schema](artifact/assets/handoff-spec.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, json, shell commands, configuration] <br>
**Output Format:** [JSON files and concise Markdown/text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a handoff spec and may produce clarifying-question JSON beside the evaluated target.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
