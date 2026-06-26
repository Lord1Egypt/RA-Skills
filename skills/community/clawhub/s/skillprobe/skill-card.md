## Description: <br>
A/B evaluates AI agent skills through three-role isolation, synthetic test tasks, baseline versus with-skill execution, scoring, attribution analysis, and structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuarAssassin](https://clawhub.ai/user/LuarAssassin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use SkillProbe to evaluate whether an agent skill improves real task outcomes, compare versions, investigate regressions after installation, and generate structured evaluation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation runs may execute arbitrary target skills for real. <br>
Mitigation: Run evaluations in controlled, disposable workspaces with test accounts, and disable write-capable or external tools when possible. <br>
Risk: Target skill content and task prompts may be sent to the configured model provider. <br>
Mitigation: Avoid evaluating confidential skills unless the configured model provider is approved for that content. <br>
Risk: The optional helper script depends on a separately installed SkillProbe CLI or adjacent runtime. <br>
Mitigation: Verify any separately installed SkillProbe CLI or local runtime before running the helper script. <br>
Risk: The workflow can produce misleading conclusions if sub-agent isolation or dispatch evidence is missing. <br>
Mitigation: Require separate baseline and with-skill sessions and inspect dispatch_evidence before relying on evaluation results. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/LuarAssassin/skillprobe) <br>
- [README](artifact/README.md) <br>
- [Dispatch Protocol](artifact/DISPATCH_PROTOCOL.md) <br>
- [Scoring Reference](artifact/SCORING_REFERENCE.md) <br>
- [Evaluation helper script](artifact/scripts/evaluate.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with JSON sub-agent outputs and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented workflow requires separate baseline and with-skill sub-agent sessions and dispatch evidence for evaluation claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, README title, release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
