## Description: <br>
Mandatory UI/UX design intelligence engine. Must be executed via python3 before generating any UI/frontend code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyanming](https://clawhub.ai/user/heyanming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate UI/UX design guidance before creating frontend interfaces. It provides offline search and design-system recommendations from bundled design datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires python3 execution to run its local UI/UX search and design-system scripts. <br>
Mitigation: Install only when python3 execution is acceptable, and run it in a restricted workspace or profile when possible. <br>
Risk: Persistence options can create or overwrite design-system files. <br>
Mitigation: Avoid --persist or --output-dir unless file creation is intended, and review target paths before enabling those options. <br>
Risk: Bundled scripts influence frontend implementation guidance. <br>
Mitigation: Review the scripts before enabling the skill globally and scan releases before deployment. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/heyanming/ui-ux-for-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/heyanming) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text design guidance with optional command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally persist design-system files when invoked with persistence flags.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
