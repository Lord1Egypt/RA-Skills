## Description: <br>
Super Calculator helps an agent answer natural-language arithmetic, finance, date, unit conversion, statistics, health metric, and equation-solving requests with calculation steps and units. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaozhao111596](https://clawhub.ai/user/xiaozhao111596) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to have an agent calculate everyday math, finance, date, statistics, health, equation, and unit-conversion questions from natural-language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate the calculator on prompts that merely contain numbers. <br>
Mitigation: Confirm the user's calculation intent when a prompt is ambiguous or when number-related text appears incidentally. <br>
Risk: Finance, health, and exchange-rate results are reference calculations and may be unsuitable for important decisions without verification. <br>
Mitigation: Verify important outputs against authoritative sources or qualified professionals before relying on them. <br>


## Reference(s): <br>
- [Formula reference guide](references/formulas.md) <br>
- [Skill README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiaozhao111596/super-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Natural-language calculation explanations with formulas, numeric results, and units] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and uses standard-library calculation helpers; finance, health, and exchange-rate outputs are reference calculations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
